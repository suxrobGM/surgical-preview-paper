"""Stems selected for the qualitative figures, behind the real-face license gate.

Every face in the scored runs is a real person from a licensed before/after dataset
("consented for AI use" per the experiment manifest). Publication in a paper is a
separate right: a stem may only flip to verified=True after its source passes
docs/real_face_checklist.md. No synthetic edited outputs exist in the current runs,
so until the gate clears (or new synthetic-face runs are generated) the qualitative
scripts emit nothing.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stem:
    face_id: str        # e.g. "real_01"
    procedure: str      # canonical procedure slug
    verified: bool      # license checklist passed for this face's source


# Teaser (Fig. 1): same face under prompt_only and masked_composite, gpt_image_2.
TEASER_FACE = Stem("real_01", "deep_plane_facelift", verified=False)

# Qualitative grid (Fig. 5): one row per procedure/model contrast.
GRID_FACES = [
    Stem("real_07", "deep_plane_facelift", verified=False),
    Stem("real_09", "deep_plane_facelift", verified=False),
    Stem("real_06_front", "rhinoplasty", verified=False),
]

# Method figure (Fig. 2): the chained run's stage1 intermediates (real_12).
METHOD_FACE = Stem("real_12", "deep_plane_facelift", verified=False)
