"""
VLM 로드/추론 코어 — Qwen2-VL / Qwen3-VL 공통 (AutoModelForImageTextToText, fp16).
이미지 1장 또는 영상(OpenCV 균일샘플 프레임)을 입력받아 텍스트를 생성하고 시간/토큰을 측정한다.

영상은 decord/av/qwen_vl_utils 없이 OpenCV 로 프레임을 뽑아
processor(videos=[[PIL frames]]) 로 직접 전달한다 (Windows 친화·의존성 최소).
"""

from __future__ import annotations

import gc
import time
from pathlib import Path
from typing import Dict, List

import cv2
import numpy as np
import torch
from PIL import Image

import config as C


# ── 로드/해제 ───────────────────────────────────────────────────
def load_vlm(hf_id: str):
    """(processor, model, load_sec) — fp16, cuda:0."""
    from transformers import AutoProcessor, AutoModelForImageTextToText
    t0 = time.time()
    processor = AutoProcessor.from_pretrained(
        hf_id, trust_remote_code=True,
        min_pixels=C.IMAGE_MIN_PIXELS, max_pixels=C.IMAGE_MAX_PIXELS,
    )
    model = AutoModelForImageTextToText.from_pretrained(
        hf_id, dtype=torch.float16, device_map="cuda:0", trust_remote_code=True,
    ).eval()
    return processor, model, round(time.time() - t0, 2)


def free_vram() -> None:
    """GPU 캐시 해제 — 호출 전 model/processor 참조를 None 으로 끊어야 실제로 비워짐."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


# ── 영상 → 프레임 ───────────────────────────────────────────────
def _to_pil(bgr: np.ndarray, max_side: int) -> Image.Image:
    h, w = bgr.shape[:2]
    scale = max_side / max(h, w)
    if scale < 1.0:
        bgr = cv2.resize(bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def video_thumbnail(video_path, max_side: int = 640):
    """영상 대표 프레임(중간 프레임)을 jpg 로 저장 → 경로 반환(이미 있으면 재사용). 실패 시 None.
    리포트 카드용 — 저장 위치는 config.VIDEO_THUMB_DIR/<stem>.jpg."""
    from pathlib import Path as _P
    video_path = _P(video_path)
    C.VIDEO_THUMB_DIR.mkdir(parents=True, exist_ok=True)
    out = C.VIDEO_THUMB_DIR / (video_path.stem + ".jpg")
    if out.exists():
        return out
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return None
    try:
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        frame = None
        if total > 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
            ok, fr = cap.read()
            if ok:
                frame = fr
        if frame is None:   # seek 실패 → 첫 프레임
            cap.release()
            cap = cv2.VideoCapture(str(video_path))
            ok, fr = cap.read()
            if ok:
                frame = fr
        if frame is None:
            return None
        h, w = frame.shape[:2]
        s = max_side / max(h, w)
        if s < 1.0:
            frame = cv2.resize(frame, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(out), frame)
        return out
    except Exception:
        return None
    finally:
        cap.release()


def sample_video_frames(path: Path, num_frames: int, max_side: int):
    """영상에서 균일 간격 num_frames 장 추출(짝수 보정). seek 실패 시 순차 디코드 폴백.
    반환: (frames, meta). meta={total_num_frames, fps, frames_indices} — Qwen3-VL 의
    정확한 타임스탬프 계산용(원본 fps·총프레임·실제 추출 인덱스)."""
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError(f"영상 열기 실패: {path}")
    fps = 0.0
    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS)) or 0.0
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        frames: List[Image.Image] = []
        idx_used: List[int] = []
        if total > 0:
            for idx in np.linspace(0, total - 1, num=num_frames).astype(int):
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
                ok, fr = cap.read()
                if ok:
                    frames.append(_to_pil(fr, max_side))
                    idx_used.append(int(idx))
        if len(frames) < 2:  # 폴백: 전체 순차 디코드 후 균일 선택
            cap.release()
            cap = cv2.VideoCapture(str(path))
            buf = []
            while len(buf) < 6000:
                ok, fr = cap.read()
                if not ok:
                    break
                buf.append(fr)
            if buf:
                sel = np.linspace(0, len(buf) - 1, num=num_frames).astype(int)
                frames = [_to_pil(buf[int(j)], max_side) for j in sel]
                idx_used = [int(j) for j in sel]
                total = len(buf)
    finally:
        cap.release()
    if not frames:
        raise RuntimeError(f"프레임 추출 실패: {path}")
    if len(frames) % 2 == 1:   # temporal_patch_size=2 정합: 마지막 프레임 복제
        frames.append(frames[-1])
        idx_used.append(idx_used[-1] if idx_used else 0)
    meta = {
        "total_num_frames": total or len(frames),
        "fps": fps if fps and fps > 0 else None,
        "frames_indices": idx_used or list(range(len(frames))),
    }
    return frames, meta


# ── 한국어 강제: CJK 한자(중국어) 토큰 차단 ──────────────────────
import re as _re

#  한자 범위(한글 U+AC00–D7A3 은 제외). 한국어 출력엔 한자가 거의 불필요하므로 차단해 중국어 혼입 방지.
_HAN_RE = _re.compile(r"[㐀-䶿一-鿿豈-﫿︰-﹏\U00020000-\U0002FA1F]")
_HAN_CACHE: dict = {}


def _han_token_ids(tokenizer):
    """토크나이저에서 '한자를 포함하는 토큰' id 목록(토크나이저당 1회 계산 후 캐시)."""
    key = id(tokenizer)
    if key not in _HAN_CACHE:
        ids = []
        for i in range(len(tokenizer)):
            try:
                if _HAN_RE.search(tokenizer.decode([i], skip_special_tokens=False)):
                    ids.append(i)
            except Exception:
                continue
        _HAN_CACHE[key] = ids
    return _HAN_CACHE[key]


def _korean_logits_processor(processor, device):
    """한자 토큰 logits 를 -inf 로 막는 LogitsProcessorList (실패/없음 시 None)."""
    try:
        from transformers import LogitsProcessor, LogitsProcessorList
    except Exception:
        return None
    tok = getattr(processor, "tokenizer", None) or processor
    ids = _han_token_ids(tok)
    if not ids:
        return None
    ban = torch.tensor(ids, dtype=torch.long, device=device)

    class _BanHan(LogitsProcessor):
        def __init__(self):
            self.bias = None   # 한자 위치 -inf bias (항목당 1회 생성, 매 스텝 재사용)

        def __call__(self, input_ids, scores):
            if self.bias is None or self.bias.shape[-1] != scores.shape[-1]:
                b = torch.zeros(scores.shape[-1], device=scores.device, dtype=scores.dtype)
                b[ban[ban < scores.shape[-1]]] = float("-inf")
                self.bias = b
            return scores + self.bias   # 벡터 덧셈 — 매 스텝 인덱스 할당보다 훨씬 빠름

    return LogitsProcessorList([_BanHan()])


# ── 추론 ────────────────────────────────────────────────────────
def _generate(processor, model, text: str, *, images=None, videos=None,
              video_metadata=None, max_new_tokens: int, temperature: float) -> Dict[str, object]:
    proc_kwargs = dict(text=[text], padding=True, return_tensors="pt")
    if images is not None:
        proc_kwargs["images"] = images
    if videos is not None:
        proc_kwargs["videos"] = videos
        # 직접 추출한 프레임을 그대로 사용 — 프로세서 내부 재샘플 차단.
        # (Qwen3-VL 영상프로세서 do_sample_frames 기본 True → 8프레임을 4로 줄이고
        #  가짜 fps=24 타임스탬프를 주입함. Qwen2-VL 은 기본 False라 8프레임 유지 →
        #  명시하지 않으면 두 모델이 4 vs 8 프레임으로 불공정 비교됨.)
        proc_kwargs["do_sample_frames"] = False
        if video_metadata is not None:   # 원본 fps·인덱스 → Qwen3-VL 타임스탬프 정확화
            proc_kwargs["video_metadata"] = video_metadata
    inputs = processor(**proc_kwargs).to(model.device)
    in_len = inputs.input_ids.shape[1]
    gen_kwargs = dict(max_new_tokens=max_new_tokens,
                      repetition_penalty=getattr(C, "REPETITION_PENALTY", 1.05))
    nrns = getattr(C, "NO_REPEAT_NGRAM_SIZE", 0)
    if nrns and nrns > 0:                       # 문장 단위 반복 루프 차단
        gen_kwargs["no_repeat_ngram_size"] = nrns
    if temperature and temperature > 0:
        gen_kwargs.update(do_sample=True, temperature=temperature)
    else:
        gen_kwargs.update(do_sample=False)
    if getattr(C, "FORCE_KOREAN", False):   # 한자(중국어) 토큰 생성 차단
        lp = _korean_logits_processor(processor, model.device)
        if lp is not None:
            gen_kwargs["logits_processor"] = lp
    t0 = time.time()
    with torch.no_grad():
        out = model.generate(**inputs, **gen_kwargs)
    elapsed = time.time() - t0
    trimmed = out[:, in_len:]
    text_out = processor.batch_decode(
        trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False,
    )[0].strip()
    n_tok = int(trimmed.shape[1])
    return {
        "text": text_out,
        "tokens": n_tok,
        "time_sec": round(elapsed, 3),
        "tok_per_sec": round(n_tok / max(elapsed, 0.001), 1),
    }


def infer_image(processor, model, image_path: Path, prompt: str,
                max_new_tokens: int, temperature: float) -> Dict[str, object]:
    image = Image.open(image_path).convert("RGB")
    messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return _generate(processor, model, text, images=[image],
                     max_new_tokens=max_new_tokens, temperature=temperature)


def infer_video(processor, model, video_path: Path, prompt: str,
                max_new_tokens: int, temperature: float) -> Dict[str, object]:
    frames, vmeta = sample_video_frames(video_path, C.VIDEO_NUM_FRAMES, C.VIDEO_FRAME_MAX_SIDE)
    messages = [{"role": "user", "content": [{"type": "video"}, {"type": "text", "text": prompt}]}]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    out = _generate(processor, model, text, videos=[frames], video_metadata=[vmeta],
                    max_new_tokens=max_new_tokens, temperature=temperature)
    out["num_frames"] = len(frames)
    return out
