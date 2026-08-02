"""Weighted merge: combine an existing N-fold quantized ensemble average with
a new member at a FRACTIONAL weight (not full 1/(N+1)), for cases where the
new member is known to be weaker (e.g. from leakage-free validation) but
might still add useful diversity at reduced influence.

combined = round((n_old*old + weight*new) / (n_old+weight)) per-pixel.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

old_dir = Path(sys.argv[1])
new_dir = Path(sys.argv[2])
out_dir = Path(sys.argv[3])
n_old = float(sys.argv[4])
weight = float(sys.argv[5])

out_dir.mkdir(parents=True, exist_ok=True)
old_paths = sorted(old_dir.glob("*.png"))
assert len(old_paths) == 50, f"expected 50 old files, got {len(old_paths)}"

for old_path in old_paths:
    name = old_path.name
    new_path = new_dir / name
    assert new_path.exists(), f"missing new prediction for {name}"

    old_img = np.array(Image.open(old_path).convert("RGB")).astype(np.float64)
    new_img = np.array(Image.open(new_path).convert("RGB")).astype(np.float64)

    combined = (n_old * old_img + weight * new_img) / (n_old + weight)
    combined = np.clip(np.round(combined), 0, 255).astype(np.uint8)

    Image.fromarray(combined, mode="RGB").save(out_dir / name, compress_level=9)

print(f"Merged {len(old_paths)} files: {n_old}x{old_dir.name} + {weight}x{new_dir.name} -> {out_dir}")
