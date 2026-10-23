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
        redact(out_dir)
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
    redact(out_dir)
    return len(list(out_dir.glob("S*.jpg")))


# Areas painted over in the published slide images (the original .pptx is never touched): the presenter's name line
# on each title slide. Box = fraction of width/height (left, top, right, bottom).
REDACT = {"S1.jpg": (0.05, 0.755, 0.62, 0.815)}


def redact(out_dir):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  slide images: Pillow missing, title-slide name not redacted")
        return
    for name, (l, t, r, b) in REDACT.items():
        f = out_dir / name
        if not f.exists():
            continue
        im = Image.open(f).convert("RGB")
        w, h = im.size
        box = (int(l * w), int(t * h), int(r * w), int(b * h))
        bg = im.getpixel((max(0, box[0] - 8), box[1] + (box[3] - box[1]) // 2))  # the slide background right beside it
        pts = [(box[0] + (box[2] - box[0]) * i // 6, box[1] + (box[3] - box[1]) // 2) for i in range(1, 6)]
        if all(sum(abs(x - y) for x, y in zip(im.getpixel(q), bg)) < 24 for q in pts):
            continue  # already painted over; don't re-save (each JPEG save loses quality)
        ImageDraw.Draw(im).rectangle(box, fill=bg)
        im.save(f, quality=80)
