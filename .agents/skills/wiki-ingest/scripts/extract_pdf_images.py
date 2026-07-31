# /// script
# requires-python = ">=3.10"
# dependencies = ["pymupdf", "click", "loguru", "pydantic"]
# ///
"""Extract text and figures from a PDF for the wiki-ingest skill.

Three subcommands, ordered cheap → expensive:

* ``text``     — dump the text layer plus per-page stats (chars / embedded images /
  vector drawings). Cheap and vision-free: run it first to transcribe text-layer pages
  and to classify each page's modality before deciding what actually needs the eyes.
* ``embedded`` — dump embedded raster images (clean photos without the surrounding
  slide). Vector figures won't appear here — use ``render`` for those.
* ``render``   — rasterize page(s), optionally cropped to a bbox, to PNG. Captures any
  figure uniformly (vector diagrams, charts, photos) and whole pages for visual reading.

Dependencies are declared inline (PEP 723), so ``uv run`` installs them on the fly::

    uv run extract_pdf_images.py text --pdf in.pdf --pages 1-5
    uv run extract_pdf_images.py render --pdf in.pdf --pages 5 \
        --out-dir wiki/images/distillation --prefix consistency-model
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import click
from loguru import logger
from pydantic import BaseModel


def import_fitz() -> Any:
    """Import PyMuPDF (``fitz``), raising an actionable error if it is missing."""
    try:
        import fitz
    except ImportError as exc:
        logger.error(
            "PyMuPDF (fitz) is not installed. Run with "
            "`uv run --with pymupdf python <script> ...` or `pip install pymupdf`. "
            "Fallback: poppler `pdftoppm` (render) / `pdfimages` (embedded)."
        )
        raise SystemExit(1) from exc
    return fitz


def parse_pages(spec: str, page_count: int) -> list[int]:
    """Parse a 1-based page spec like ``'4,7-9'`` into valid page numbers."""
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            pages.update(range(int(start), int(end) + 1))
        else:
            pages.add(int(part))
    valid = sorted(page for page in pages if 1 <= page <= page_count)
    if not valid:
        raise click.BadParameter(
            f"No valid pages in '{spec}' for a {page_count}-page PDF"
        )
    return valid


def parse_bbox(spec: str | None) -> list[float] | None:
    """Parse an ``x0,y0,x1,y1`` crop specification into four floats."""
    if spec is None:
        return None
    parts = [float(value) for value in spec.split(",")]
    if len(parts) != 4:
        raise click.BadParameter("bbox must be 'x0,y0,x1,y1' in PDF points")
    return parts


class TextConfig(BaseModel):
    """Parameters for the ``text`` command."""

    pdf: Path
    pages: str | None = None
    mode: str = "text"


class RenderConfig(BaseModel):
    """Parameters for the ``render`` command."""

    pdf: Path
    pages: str
    out_dir: Path
    prefix: str
    dpi: int = 200
    bbox: str | None = None


class EmbeddedConfig(BaseModel):
    """Parameters for the ``embedded`` command."""

    pdf: Path
    out_dir: Path
    prefix: str
    min_size: int = 64


def page_text(page: Any, mode: str) -> str:
    """Return a page's plain text or text with block separation."""
    if mode == "blocks":
        blocks = page.get_text("blocks")
        return "\n\n".join(block[4].strip() for block in blocks if block[4].strip())
    return page.get_text("text")


def extract_text(config: TextConfig) -> str:
    """Dump the text layer and per-page modality statistics."""
    fitz = import_fitz()
    document = fitz.open(config.pdf)
    page_numbers = (
        parse_pages(config.pages, document.page_count)
        if config.pages
        else list(range(1, document.page_count + 1))
    )
    chunks: list[str] = []
    for page_number in page_numbers:
        page = document[page_number - 1]
        plain = page.get_text("text")
        image_count = len(page.get_images(full=True))
        drawing_count = len(page.get_drawings())
        chunks.append(
            f"=== page {page_number} | chars={len(plain)} "
            f"images={image_count} drawings={drawing_count} ==="
        )
        chunks.append(page_text(page, config.mode))
    document.close()
    return "\n".join(chunks)


def render_pages(config: RenderConfig) -> list[Path]:
    """Rasterize the requested pages and return the written PNG paths."""
    fitz = import_fitz()
    document = fitz.open(config.pdf)
    page_numbers = parse_pages(config.pages, document.page_count)
    bbox = parse_bbox(config.bbox)
    config.out_dir.mkdir(parents=True, exist_ok=True)
    matrix = fitz.Matrix(config.dpi / 72, config.dpi / 72)
    single_page = len(page_numbers) == 1
    written: list[Path] = []
    for page_number in page_numbers:
        page = document[page_number - 1]
        clip = fitz.Rect(*bbox) if bbox else None
        pixmap = page.get_pixmap(matrix=matrix, clip=clip)
        name = (
            f"{config.prefix}.png"
            if single_page
            else f"{config.prefix}-p{page_number}.png"
        )
        output_path = config.out_dir / name
        pixmap.save(output_path)
        written.append(output_path)
        logger.info(f"Rendered page {page_number} → {output_path}")
    document.close()
    return written


def extract_embedded(config: EmbeddedConfig) -> list[Path]:
    """Extract embedded raster images and return the written paths."""
    fitz = import_fitz()
    document = fitz.open(config.pdf)
    config.out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    seen: set[int] = set()
    for page in document:
        for image in page.get_images(full=True):
            xref = image[0]
            if xref in seen:
                continue
            seen.add(xref)
            base = document.extract_image(xref)
            if base["width"] < config.min_size or base["height"] < config.min_size:
                continue
            output_path = (
                config.out_dir
                / f"{config.prefix}-{len(written) + 1:02d}.{base['ext']}"
            )
            output_path.write_bytes(base["image"])
            written.append(output_path)
            logger.info(f"Extracted embedded image xref={xref} → {output_path}")
    document.close()
    if not written:
        logger.warning(
            "No embedded raster images passed the size filter; "
            "for vector figures, try `render`."
        )
    return written


@click.group()
def cli() -> None:
    """Extract text and figures from a PDF for the wiki-ingest skill."""


@cli.command()
@click.option("--pdf", required=True, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--pages",
    default=None,
    help="1-based page spec, e.g. '5' or '4,7-9'; all pages if omitted",
)
@click.option(
    "--mode",
    default="text",
    show_default=True,
    type=click.Choice(["text", "blocks"]),
    help="'text' is a plain dump; 'blocks' keeps per-block layout separation",
)
def text(pdf: Path, pages: str | None, mode: str) -> None:
    """Dump the text layer and per-page modality statistics."""
    config = TextConfig(pdf=pdf, pages=pages, mode=mode)
    click.echo(extract_text(config))


@cli.command()
@click.option("--pdf", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--pages", required=True, help="1-based page spec, e.g. '5' or '4,7-9'")
@click.option("--out-dir", required=True, type=click.Path(path_type=Path))
@click.option("--prefix", required=True, help="Filename prefix for the written PNGs")
@click.option("--dpi", default=200, show_default=True, type=int)
@click.option("--bbox", default=None, help="Optional crop 'x0,y0,x1,y1' in PDF points")
def render(
    pdf: Path,
    pages: str,
    out_dir: Path,
    prefix: str,
    dpi: int,
    bbox: str | None,
) -> None:
    """Rasterize pages, optionally cropped to a bounding box, as PNG."""
    config = RenderConfig(
        pdf=pdf,
        pages=pages,
        out_dir=out_dir,
        prefix=prefix,
        dpi=dpi,
        bbox=bbox,
    )
    for path in render_pages(config):
        click.echo(path)


@cli.command()
@click.option("--pdf", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--out-dir", required=True, type=click.Path(path_type=Path))
@click.option("--prefix", required=True, help="Filename prefix for the written images")
@click.option(
    "--min-size",
    default=64,
    show_default=True,
    type=int,
    help="Skip images smaller than this size in pixels",
)
def embedded(pdf: Path, out_dir: Path, prefix: str, min_size: int) -> None:
    """Extract embedded raster images above the size threshold."""
    config = EmbeddedConfig(
        pdf=pdf,
        out_dir=out_dir,
        prefix=prefix,
        min_size=min_size,
    )
    for path in extract_embedded(config):
        click.echo(path)


if __name__ == "__main__":
    cli()
