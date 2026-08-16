"""Perform cross-platform structural checks on the rendered architecture diagram."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIAGRAM = ROOT / "docs" / "architecture" / "tm1-architecture.png"


def main() -> None:
    with Image.open(DIAGRAM) as image:
        assert image.format == "PNG", "Architecture asset must be a PNG"
        assert image.size == (1800, 1160), f"Unexpected diagram dimensions: {image.size}"
        assert image.mode in {"RGB", "RGBA"}, f"Unexpected diagram mode: {image.mode}"

        extrema = image.convert("RGB").getextrema()
        assert any(low < high for low, high in extrema), "Diagram appears blank"

    print("PASS: architecture diagram is a nonblank 1800 x 1160 PNG.")


if __name__ == "__main__":
    main()
