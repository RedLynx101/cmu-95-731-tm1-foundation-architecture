from __future__ import annotations

import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "architecture" / "tm1-architecture.png"


@dataclass(frozen=True)
class Palette:
    fill: str
    border: str
    text: str
    badge_fill: str


PALETTES = {
    "implemented": Palette("#E9F4EF", "#176B5B", "#102A25", "#CDE8DE"),
    "candidate": Palette("#EEF3FA", "#315F8C", "#172B3D", "#D9E5F2"),
    "future": Palette("#FFF5DF", "#9B6816", "#4A3512", "#F5E3B8"),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for name in names:
        path = Path(name)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


TITLE_FONT = font(42, bold=True)
SUBTITLE_FONT = font(21)
AUTHOR_FONT = font(18, bold=True)
BOX_TITLE_FONT = font(22, bold=True)
BOX_BODY_FONT = font(17)
BADGE_FONT = font(13, bold=True)
LEGEND_FONT = font(16)


def centered_text(
    draw: ImageDraw.ImageDraw,
    bounds: tuple[int, int, int, int],
    value: str,
    selected_font: ImageFont.ImageFont,
    fill: str,
) -> None:
    left, top, right, bottom = bounds
    text_bounds = draw.multiline_textbbox(
        (0, 0), value, font=selected_font, spacing=5, align="center"
    )
    width = text_bounds[2] - text_bounds[0]
    height = text_bounds[3] - text_bounds[1]
    draw.multiline_text(
        ((left + right - width) / 2, (top + bottom - height) / 2),
        value,
        font=selected_font,
        fill=fill,
        spacing=5,
        align="center",
    )


def draw_box(
    draw: ImageDraw.ImageDraw,
    bounds: tuple[int, int, int, int],
    title: str,
    body: str,
    category: str,
) -> None:
    colors = PALETTES[category]
    left, top, right, bottom = bounds
    draw.rounded_rectangle(bounds, radius=10, fill=colors.fill, outline=colors.border, width=3)

    badge = category.upper()
    badge_bounds = draw.textbbox((0, 0), badge, font=BADGE_FONT)
    badge_width = badge_bounds[2] - badge_bounds[0] + 22
    draw.rounded_rectangle(
        (left + 14, top + 13, left + 14 + badge_width, top + 38),
        radius=6,
        fill=colors.badge_fill,
    )
    draw.text((left + 25, top + 17), badge, font=BADGE_FONT, fill=colors.text)

    wrapped_title = "\n".join(textwrap.wrap(title, width=22))
    wrapped_body = "\n".join(textwrap.wrap(body, width=31))
    centered_text(
        draw,
        (left + 12, top + 44, right - 12, top + 91),
        wrapped_title,
        BOX_TITLE_FONT,
        colors.text,
    )
    centered_text(
        draw,
        (left + 14, top + 90, right - 14, bottom - 10),
        wrapped_body,
        BOX_BODY_FONT,
        colors.text,
    )


def arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str = "#4B5563",
    dashed: bool = False,
) -> None:
    if dashed:
        x1, y1 = start
        x2, y2 = end
        segments = 13
        for i in range(segments):
            if i % 2 == 0:
                t1 = i / segments
                t2 = min((i + 1) / segments, 1)
                draw.line(
                    (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1,
                     x1 + (x2 - x1) * t2, y1 + (y2 - y1) * t2),
                    fill=color,
                    width=4,
                )
    else:
        draw.line((start, end), fill=color, width=4)

    x2, y2 = end
    x1, y1 = start
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 > x1 else -1
        points = [(x2, y2), (x2 - 16 * direction, y2 - 9), (x2 - 16 * direction, y2 + 9)]
    else:
        direction = 1 if y2 > y1 else -1
        points = [(x2, y2), (x2 - 9, y2 - 16 * direction), (x2 + 9, y2 - 16 * direction)]
    draw.polygon(points, fill=color)


def main() -> None:
    image = Image.new("RGB", (1800, 1160), "#FAFBFC")
    draw = ImageDraw.Draw(image)

    draw.text((70, 50), "TM1 Foundation Architecture", font=TITLE_FONT, fill="#14212B")
    draw.text(
        (72, 108),
        (
            "Solid flow: current application and AWS deployment candidate | "
            "Dashed flow: later milestone"
        ),
        font=SUBTITLE_FONT,
        fill="#4B5563",
    )
    draw.text(
        (72, 151),
        "Team: Noah Hicks and Taha Zakir",
        font=AUTHOR_FONT,
        fill="#374151",
    )

    boxes = {
        "client": (55, 305, 315, 465),
        "api": (360, 305, 620, 465),
        "lambda": (665, 305, 925, 465),
        "adapter": (970, 305, 1230, 465),
        "stub": (1275, 245, 1735, 405),
        "model": (1275, 485, 1735, 645),
        "iam": (360, 720, 620, 880),
        "cloudwatch": (665, 720, 925, 880),
        "s3": (970, 720, 1230, 880),
        "secrets": (1275, 720, 1735, 880),
    }

    arrow(draw, (315, 385), (360, 385))
    arrow(draw, (620, 385), (665, 385))
    arrow(draw, (925, 385), (970, 385))
    arrow(draw, (1230, 365), (1275, 325))
    arrow(draw, (1230, 410), (1275, 565), color="#9B6816", dashed=True)
    arrow(draw, (795, 465), (795, 720))
    arrow(draw, (490, 720), (665, 445), color="#315F8C")
    arrow(draw, (1100, 720), (855, 465), color="#9B6816", dashed=True)
    arrow(draw, (1505, 720), (1505, 645), color="#9B6816", dashed=True)

    draw_box(draw, boxes["client"], "Client", "Sends a question over HTTPS", "implemented")
    draw_box(draw, boxes["api"], "Amazon API Gateway", "Routes /ask and /health", "candidate")
    draw_box(draw, boxes["lambda"], "AWS Lambda", "Runs FastAPI through Mangum", "candidate")
    draw_box(
        draw,
        boxes["adapter"],
        "Model Adapter",
        "Keeps the API provider-neutral",
        "implemented",
    )
    draw_box(draw, boxes["stub"], "Stub Provider", "Deterministic TM1 response path", "implemented")
    draw_box(draw, boxes["model"], "Bedrock or External Model", "Future answer provider", "future")
    draw_box(draw, boxes["iam"], "AWS IAM", "Least-privilege execution role", "candidate")
    draw_box(
        draw,
        boxes["cloudwatch"],
        "Amazon CloudWatch",
        "Request, error, and latency evidence",
        "candidate",
    )
    draw_box(draw, boxes["s3"], "Amazon S3", "Future approved source documents", "future")
    draw_box(
        draw,
        boxes["secrets"],
        "Secrets Manager or Parameter Store",
        "Future external credentials",
        "future",
    )

    draw.line((55, 970, 1735, 970), fill="#D1D5DB", width=2)
    legend_items = [
        ("implemented", "Implemented and locally testable"),
        ("candidate", "AWS deployment candidate; Learner Lab check pending"),
        ("future", "Future integration, not part of TM1"),
    ]
    x = 75
    for category, label in legend_items:
        colors = PALETTES[category]
        draw.rounded_rectangle(
            (x, 1025, x + 28, 1053),
            radius=5,
            fill=colors.fill,
            outline=colors.border,
            width=2,
        )
        draw.text((x + 40, 1026), label, font=LEGEND_FONT, fill="#374151")
        x += 540

    draw.text(
        (75, 1100),
        (
            "TM1 scope: stable contract, deterministic provider, tests, "
            "and deployable infrastructure source."
        ),
        font=LEGEND_FONT,
        fill="#4B5563",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
