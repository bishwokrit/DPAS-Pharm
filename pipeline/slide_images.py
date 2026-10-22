"""Render each lecture slide to an image (docs/<LEC>/slides/S<n>.jpg) so Sidekick can show the source slide.
Uses LibreOffice (pptx -> pdf) and pdftoppm (pdf -> jpg). Skips work when images are newer than the pptx."""
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render(lid, out_dir):
    pptx = next((ROOT / "inputs" / "lectures" / lid).glob("*.pptx"), None)
    if not pptx:
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    done = sorted(out_dir.glob("S*.jpg"))
    if done and min(p.stat().st_mtime for p in done) > pptx.stat().st_mtime:
        return len(done)
    if not (shutil.which("soffice") and shutil.which("pdftoppm")):
        print("  slide images: skipped (needs LibreOffice and poppler)")
        return len(done)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(pptx)],
                       check=True, capture_output=True, timeout=600)
        pdf = next(Path(tmp).glob("*.pdf"))
        subprocess.run(["pdftoppm", "-jpeg", "-jpegopt", "quality=72", "-scale-to-x", "1100", "-scale-to-y", "-1",
                        str(pdf), str(Path(tmp) / "s")], check=True, timeout=600)
        for old in out_dir.glob("S*.jpg"):
            old.unlink()
        for img in Path(tmp).glob("s-*.jpg"):
            shutil.move(img, out_dir / f"S{int(img.stem.split('-')[-1])}.jpg")
    return len(list(out_dir.glob("S*.jpg")))
