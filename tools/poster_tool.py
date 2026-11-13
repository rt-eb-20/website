"""Helper for the poster & paper pages under p/<slug>/.

Run from the website folder:

    python tools/poster_tool.py qr web26
        -> p/web26/qr.svg (print, vector) and p/web26/qr.png
           encoding https://theuerkauf.me/p/web26/

    python tools/poster_tool.py images web26
        -> p/web26/poster.webp (page preview), poster-thumb.webp (Research list)
           and og.jpg (link preview on LinkedIn etc.), all rendered from
           p/web26/theuerkauf-web26-poster.pdf

One-time setup:  python -m pip install segno pymupdf pillow

This folder is only a local helper; the website does not need it.
"""

import argparse
import io
import sys
from pathlib import Path

SITE = "https://theuerkauf.me"
ROOT = Path(__file__).resolve().parent.parent


def make_qr(slug: str, dark: str) -> None:
    import segno

    url = f"{SITE}/p/{slug}/"
    out = ROOT / "p" / slug
    out.mkdir(parents=True, exist_ok=True)
    # Error level Q survives ~25 % damage (glare, scratches); border=4 is the
    # quiet zone the QR standard asks for. Keep it white when you place the code.
    qr = segno.make(url, error="q", micro=False)
    qr.save(out / "qr.svg", border=4, dark=dark, light="#ffffff", scale=10)
    qr.save(out / "qr.png", border=4, dark=dark, light="#ffffff", scale=40)
    print(f"{url}\n  QR version {qr.version} ({qr.symbol_size(scale=1, border=0)[0]} modules), "
          f"error level {qr.error}\n  -> {out / 'qr.svg'}\n  -> {out / 'qr.png'}")


def make_images(slug: str, pdf_name: str | None) -> None:
    import pymupdf
    from PIL import Image

    folder = ROOT / "p" / slug
    pdf = folder / (pdf_name or f"theuerkauf-{slug}-poster.pdf")
    if not pdf.exists():
        sys.exit(f"Poster PDF not found: {pdf}")
    page = pymupdf.open(pdf)[0]

    def render(width: int) -> Image.Image:
        # Render 25 % larger, then downscale: keeps small poster text crisp.
        zoom = width * 1.25 / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        return img.resize((width, round(width * img.height / img.width)), Image.LANCZOS)

    preview = render(1600)
    preview.save(folder / "poster.webp", quality=80, method=6)
    thumb = render(480)
    thumb.save(folder / "poster-thumb.webp", quality=80, method=6)
    # Link preview (1200 x 630): top of the poster (title block), framed by a
    # 15 px strip in the poster's own background colour.
    og = render(1200)
    canvas = Image.new("RGB", (1200, 630), og.getpixel((5, 5)))
    canvas.paste(og.crop((0, 0, 1200, min(600, og.height))), (0, 15))
    canvas.save(folder / "og.jpg", quality=85, optimize=True, progressive=True)

    print(f"Rendered from {pdf.name}:\n"
          f"  poster.webp        {preview.width} x {preview.height}\n"
          f"  poster-thumb.webp  {thumb.width} x {thumb.height}\n"
          f"  og.jpg             1200 x 630\n"
          "If the poster's proportions changed, update the width/height\n"
          "attributes of the <img> tags in p/<slug>/index.html and research.html.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    q = sub.add_parser("qr", help="QR code for https://theuerkauf.me/p/<slug>/")
    q.add_argument("slug")
    q.add_argument("--dark", default="#000000", help="module colour (default black)")
    i = sub.add_parser("images", help="preview images from the poster PDF")
    i.add_argument("slug")
    i.add_argument("--pdf", help="PDF file name inside p/<slug>/ (default theuerkauf-<slug>-poster.pdf)")
    args = parser.parse_args()
    if args.command == "qr":
        make_qr(args.slug, args.dark)
    else:
        make_images(args.slug, args.pdf)


if __name__ == "__main__":
    main()
