"""Qualitative figure grids (PIL) from run images, honoring the real-face license gate.

Builds, for each verified stem, side-by-side panels: input | prompt-only | masked
composite (teaser), and multi-row grids for the qualitative figure. Skips (with a
message) any stem whose source has not passed docs/real_face_checklist.md.
"""

from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from config import DATA_DIR, FIGURES_DIR, MODEL_NAMES, POC_ROOT
from figure_stems import GRID_FACES, STRIP_FACE, STRIP_MODELS, TEASER_FACE

PANEL = 384      # px per face panel
RUNS = POC_ROOT / "outputs" / "runs"


def load_rows() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "canonical_rows.csv")


def find_row(df: pd.DataFrame, face_id: str, procedure: str, control: str):
    g = df[(df.face_id == face_id) & (df.procedure == procedure) & (df.control == control)]
    return None if g.empty else g.iloc[0]


def image_for(row) -> Path:
    return RUNS / row.run_id / "images" / f"{row.stem}.png"


def input_for(face_id: str, procedure: str) -> Path:
    return POC_ROOT / "data" / "faces" / procedure / f"{face_id}.png"


def panel(img_path: Path, label: str, label_size: int = 16) -> Image.Image:
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((PANEL, PANEL))
    label_h = label_size + 12
    canvas = Image.new("RGB", (PANEL, PANEL + label_h), "white")
    canvas.paste(img, ((PANEL - img.width) // 2, 0))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", label_size)
    except OSError:
        font = ImageFont.load_default()
    w = draw.textlength(label, font=font)
    draw.text(((PANEL - w) // 2, PANEL + 5), label, fill="#0b0b0b", font=font)
    return canvas


def hstack(panels: list[Image.Image], gap: int = 6) -> Image.Image:
    w = sum(p.width for p in panels) + gap * (len(panels) - 1)
    h = max(p.height for p in panels)
    out = Image.new("RGB", (w, h), "white")
    x = 0
    for p in panels:
        out.paste(p, (x, 0))
        x += p.width + gap
    return out


def make_teaser(df: pd.DataFrame) -> bool:
    s = TEASER_FACE
    if not s.verified:
        print(f"teaser: {s.face_id} not license-verified - skipped")
        return False
    po = find_row(df, s.face_id, s.procedure, "prompt_only")
    mc = find_row(df, s.face_id, s.procedure, "masked_composite")
    if po is None or mc is None:
        print(f"teaser: missing control rows for {s.face_id}")
        return False
    img = hstack([
        panel(input_for(s.face_id, s.procedure), "Input"),
        panel(image_for(po), "Prompt only"),
        panel(image_for(mc), "Masked composite"),
    ])
    img.save(FIGURES_DIR / "teaser_triptych.png")
    return True


def make_grid(df: pd.DataFrame) -> bool:
    rows = []
    for s in GRID_FACES:
        if not s.verified:
            print(f"grid: {s.face_id} not license-verified - skipped")
            continue
        panels = [panel(input_for(s.face_id, s.procedure), "Input")]
        for control in ("prompt_only", "masked_composite", "masked_inpaint"):
            r = find_row(df, s.face_id, s.procedure, control)
            if r is not None and image_for(r).exists():
                panels.append(panel(image_for(r), control.replace("_", " ").capitalize()))
        if len(panels) > 1:
            rows.append(hstack(panels))
        else:
            print(f"grid: {s.face_id}/{s.procedure} has no rows in the canonical set - skipped")
    if not rows:
        return False
    w = max(r.width for r in rows)
    h = sum(r.height for r in rows) + 6 * (len(rows) - 1)
    out = Image.new("RGB", (w, h), "white")
    y = 0
    for r in rows:
        out.paste(r, (0, y))
        y += r.height + 6
    out.save(FIGURES_DIR / "qualitative_grid.png")
    return True


def make_model_strip(df: pd.DataFrame) -> bool:
    """The same face composited by every editor: the model-comparison figure."""
    s = STRIP_FACE
    if not s.verified:
        print(f"strip: {s.face_id} not license-verified - skipped")
        return False
    panels = [panel(input_for(s.face_id, s.procedure), "Input", label_size=36)]
    for model in STRIP_MODELS:
        g = df[(df.face_id == s.face_id) & (df.procedure == s.procedure)
               & (df.control == "masked_composite") & (df.model == model)]
        if g.empty or not image_for(g.iloc[0]).exists():
            print(f"strip: no composited {model} edit for {s.face_id} - skipped")
            continue
        panels.append(panel(image_for(g.iloc[0]), MODEL_NAMES.get(model, model), label_size=36))
    if len(panels) < 3:
        return False
    hstack(panels).save(FIGURES_DIR / "model_strip.png")
    return True


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = load_rows()
    made = [make_teaser(df), make_grid(df), make_model_strip(df)]
    if not any(made):
        print("no qualitative figures generated - real-face gate is closed "
              "(see docs/real_face_checklist.md)")


if __name__ == "__main__":
    main()
