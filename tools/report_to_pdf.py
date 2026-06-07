"""
벤치마크 마크다운 리포트 → 이미지 포함 PDF.
  md → HTML(이미지 base64 인라인 + <details> 펼침) → MS Edge/Chrome 헤드리스 print-to-pdf.
별도 PDF 라이브러리 설치 없이 Windows 기본 Edge 로 변환(이미지·한글 폰트 그대로 렌더).

사용: venv\\Scripts\\python.exe tools\\report_to_pdf.py [md경로]
      (생략 시 results/ 의 최신 vlm_benchmark_*.md)
"""

from __future__ import annotations

import base64
import glob
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from markdown_it import MarkdownIt

VLM_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = VLM_DIR / "results"

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".webp": "image/webp", ".bmp": "image/bmp", ".gif": "image/gif"}

CSS = """
@page { size: A4; margin: 12mm; }
body { font-family: 'Malgun Gothic','맑은 고딕',sans-serif; font-size: 11px; line-height: 1.55; color: #222; }
h1 { font-size: 19px; border-bottom: 2px solid #333; padding-bottom: 4px; }
h2 { font-size: 15px; margin-top: 18px; border-bottom: 1px solid #ccc; padding-bottom: 2px; }
h3 { font-size: 13px; margin-top: 12px; }
h4 { font-size: 12px; margin: 8px 0 2px; color: #114; }
table { border-collapse: collapse; width: 100%; font-size: 10px; margin: 6px 0; }
th, td { border: 1px solid #bbb; padding: 3px 6px; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
img { max-width: 360px; max-height: 270px; border: 1px solid #ddd; border-radius: 3px; margin: 4px 0; page-break-inside: avoid; }
details { margin: 8px 0; border: 1px solid #eee; border-radius: 4px; padding: 4px 10px; }
summary { font-weight: bold; color: #225; }
blockquote { color: #555; border-left: 3px solid #ddd; margin: 6px 0; padding: 2px 10px; background: #fafafa; }
code { background: #f3f3f3; padding: 1px 3px; border-radius: 3px; font-size: 10px; }
h4, tr, blockquote { page-break-inside: avoid; }
/* 캡처별 이미지+해석 카드 */
.capture { display: flex; gap: 12px; border: 1px solid #ddd; border-radius: 5px; padding: 8px; margin: 8px 0; page-break-inside: avoid; background: #fff; }
.cap-img { flex: 0 0 280px; }
.cap-img img { width: 280px; max-height: 210px; object-fit: contain; border: 1px solid #ccc; border-radius: 3px; margin: 0; }
.cap-body { flex: 1; min-width: 0; }
.cap-head { font-weight: bold; font-size: 10.5px; color: #114; margin-bottom: 4px; border-bottom: 1px dashed #ccc; padding-bottom: 3px; }
.cap-text { font-size: 10.5px; line-height: 1.7; }
.cap-label { font-weight: bold; color: #fff; background: #3b5bdb; padding: 1px 6px; border-radius: 3px; margin-right: 4px; font-size: 9.5px; }
.v-danger { color: #c0392b; font-weight: bold; }
.v-safe { color: #1e7e34; font-weight: bold; }
.noimg { width: 280px; height: 160px; display: flex; align-items: center; justify-content: center; color: #999; border: 1px dashed #ccc; }
"""

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_browser() -> str | None:
    import shutil
    for c in EDGE_CANDIDATES:
        if os.path.exists(c):
            return c
    return shutil.which("msedge") or shutil.which("chrome")


def embed_images(html: str, base_dir: Path) -> tuple[str, int]:
    n = 0

    def repl(m):
        nonlocal n
        src = m.group(1)
        if src.startswith(("data:", "http://", "https://")):
            return m.group(0)
        p = (base_dir / src).resolve()
        if not p.exists():
            return m.group(0)
        mime = MIME.get(p.suffix.lower(), "image/jpeg")
        b64 = base64.b64encode(p.read_bytes()).decode()
        n += 1
        return f'src="data:{mime};base64,{b64}"'

    return re.sub(r'src="([^"]+)"', repl, html), n


def convert_one(md_path: Path, browser: str) -> bool:
    md_path = md_path.resolve()   # as_uri() 는 절대경로 필요
    md = MarkdownIt("commonmark", {"html": True}).enable("table")
    body = md.render(md_path.read_text(encoding="utf-8"))
    body = body.replace("<details>", "<details open>")     # PDF 에선 접힘 펼치기
    body, n_img = embed_images(body, md_path.parent)        # 캡처 이미지 상대경로 기준 = md 위치
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body>{body}</body></html>')
    html_path = md_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")
    pdf_path = md_path.with_suffix(".pdf")

    profile = tempfile.mkdtemp(prefix="edgepdf_")
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--hide-scrollbars",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ]
    print(f"PDF 생성 중: {md_path.name} (이미지 {n_img}장) …")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    except Exception as e:
        print(f"  [실패] 브라우저 실행 오류: {e}  (HTML 유지: {html_path})")
        return False
    finally:
        import shutil as _sh
        _sh.rmtree(profile, ignore_errors=True)

    if pdf_path.exists() and pdf_path.stat().st_size > 0:
        print(f"  [완료] {pdf_path.name}  ({pdf_path.stat().st_size // 1024} KB)")
        html_path.unlink(missing_ok=True)
        return True
    print(f"  [실패] PDF 미생성. stderr: {(r.stderr or '')[:300]}  (HTML 유지: {html_path})")
    return False


def main():
    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    else:   # results/ 와 그 하위(prompt_test, pixel_frame_test) 모두 재귀 탐색
        targets = [Path(p) for p in sorted(
            glob.glob(str(RESULTS_DIR / "**" / "vlm_benchmark_*.md"), recursive=True))]
    targets = [p for p in targets if p.exists()]
    if not targets:
        print("[중단] 변환할 vlm_benchmark_*.md 가 없습니다.")
        sys.exit(1)

    browser = find_browser()
    if not browser:
        print("[실패] Edge/Chrome 실행파일을 못 찾았습니다.")
        sys.exit(1)
    print(f"브라우저: {Path(browser).name} · 대상 {len(targets)}개")
    ok = sum(convert_one(p, browser) for p in targets)
    print(f"완료: {ok}/{len(targets)} PDF 생성")
    if ok < len(targets):
        sys.exit(1)


if __name__ == "__main__":
    main()
