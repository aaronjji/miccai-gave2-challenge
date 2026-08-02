"""Weighted-average merge: combine an existing N-fold quantized ensemble
prediction with a newly-inferred single-fold (or k-fold) prediction, without
re-running inference on the folds already baked into the old average.

combined = round((n_old*old + n_new*new) / (n_old+n_new)) per-pixel, per-channel.
Small quantization rounding error vs a from-scratch (n_old+n_new)-way average
(each input is already 8-bit quantized), but avoids re-inferring folds whose
predictions haven't changed -- the only practical way to keep growing the
ensemble under this project's local GPU / time constraints.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

old_dir = Path(sys.argv[1])
new_dir = Path(sys.argv[2])
out_dir = Path(sys.argv[3])
n_old = int(sys.argv[4])
n_new = int(sys.argv[5])

out_dir.mkdir(parents=True, exist_ok=True)
old_paths = sorted(old_dir.glob("*.png"))
assert len(old_paths) == 50, f"expected 50 old files, got {len(old_paths)}"

for old_path in old_paths:
    name = old_path.name
    new_path = new_dir / name
    assert new_path.exists(), f"missing new prediction for {name}"

    old_img = np.array(Image.open(old_path).convert("RGB")).astype(np.float64)
    new_img = np.array(Image.open(new_path).convert("RGB")).astype(np.float64)

    combined = (n_old * old_img + n_new * new_img) / (n_old + n_new)
    combined = np.clip(np.round(combined), 0, 255).astype(np.uint8)

    Image.fromarray(combined, mode="RGB").save(out_dir / name, compress_level=9)

print(f"Merged {len(old_paths)} files: {n_old}x{old_dir.name} + {n_new}x{new_dir.name} -> {out_dir}")
