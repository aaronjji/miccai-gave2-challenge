"""Compute Task 3 vascular biomarkers from Task 1/2 AV predictions.

Usage:
    python src/run_task3.py --av-dir predictions/task1/validation \
        --images-dir data/raw/GAVE2_preliminary/validation/images \
        --masks-dir data/raw/GAVE2_preliminary/validation/masks \
        --out-dir predictions/task3/validation
"""
import argparse
import sys
import traceback
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from biomarkers.compute import compute_biomarkers  # noqa: E402
from od_localization.segformer_od import find_od_segformer  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--av-dir", type=str, required=True, help="Directory of prediction-format AV PNGs (R=artery,G=vessel,B=vein)")
    p.add_argument("--images-dir", type=str, required=True, help="Original CFP images (for heuristic OD detection)")
    p.add_argument("--masks-dir", type=str, required=True, help="ROI masks (for heuristic OD detection)")
    p.add_argument("--out-dir", type=str, required=True)
    p.add_argument("--threshold", type=int, default=127, help="Fallback threshold for any channel not given its own override")
    p.add_argument("--threshold-r", type=int, default=None, help="Artery (R) channel threshold override")
    p.add_argument("--threshold-g", type=int, default=None, help="Vessel (G) channel threshold override -- feeds BOTH artery_mask and vein_mask (g & ~b / g & ~r)")
    p.add_argument("--threshold-b", type=int, default=None, help="Vein (B) channel threshold override")
    args = p.parse_args()

    thr_r = args.threshold_r if args.threshold_r is not None else args.threshold
    thr_g = args.threshold_g if args.threshold_g is not None else args.threshold
    thr_b = args.threshold_b if args.threshold_b is not None else args.threshold

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    av_dir = Path(args.av_dir)
    images_dir = Path(args.images_dir)
    masks_dir = Path(args.masks_dir)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"OD detector device: {device}")

    av_paths = sorted(av_dir.glob("*.png"))
    print(f"Computing Task3 biomarkers for {len(av_paths)} cases -> {out_dir}")
    for av_path in av_paths:
        name = av_path.stem
        try:
            av_prob = np.array(Image.open(av_path).convert("RGB"))
            av_bin = np.zeros_like(av_prob, dtype=np.uint8)
            av_bin[..., 0] = (av_prob[..., 0] > thr_r).astype(np.uint8) * 255
            av_bin[..., 1] = (av_prob[..., 1] > thr_g).astype(np.uint8) * 255
            av_bin[..., 2] = (av_prob[..., 2] > thr_b).astype(np.uint8) * 255

            image = np.array(Image.open(images_dir / f"{name}.png").convert("RGB"))
            roi = np.array(Image.open(masks_dir / f"{name}.png").convert("L"))
            od_mask = find_od_segformer(image, device=device)
            od_mask[roi == 0] = 0  # clip to field-of-view in case the model fires outside it

            result = compute_biomarkers(av_bin, od_mask)

            txt_path = out_dir / f"{name}.txt"
            with open(txt_path, "w") as f:
                for key in ["AVR", "artery_density", "vein_density", "artery_fractal_dimension", "vein_fractal_dimension"]:
                    value = result[key]
                    if isinstance(value, float) and (value != value or abs(value) == float("inf")):
                        f.write(f"{key} 0.0\n")
                    else:
                        f.write(f"{key} {value:.6f}\n")
            print(f"  {name}: OK")
        except Exception as e:
            print(f"  {name}: FAILED ({e})")
            traceback.print_exc()
            # Write a zero-valued fallback so the submission stays complete.
            with open(out_dir / f"{name}.txt", "w") as f:
                for key in ["AVR", "artery_density", "vein_density", "artery_fractal_dimension", "vein_fractal_dimension"]:
                    f.write(f"{key} 0.0\n")


if __name__ == "__main__":
    main()
