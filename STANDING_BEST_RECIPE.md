# Standing best submission recipe

Round score: **7.06756** (submissions_log.csv row 16, `task2-fold3-w03.zip`).

## Components

- **Task1**: 11-fold ensemble + horizontal-flip TTA (seed=77 folds 0-4, seed=101 folds 0-4, seed=202 fold0)
- **Task2**: same 11-fold ensemble, plus seed=202 fold3's Task2 checkpoint blended in at weight 0.3
- **Task3**: sourced from the 5-fold Task1 ensemble only (seed=77 folds 0-4), binarized at threshold=140 (~0.55) instead of the default 127

## Checkpoints used

Task1 11-fold ensemble (in order fold0..fold10):
```
runs/task1/fold{0..4}/final.pth          # seed=77
runs/task1_altseed/fold{0..4}/final.pth  # seed=101
runs/task1_seed202/fold0/final.pth       # seed=202
```

Task2 11-fold ensemble (same fold order as Task1):
```
runs/task2/fold{0..4}/final.pth
runs/task2_altseed/fold{0..4}/final.pth
runs/task2_seed202/fold0/final.pth
```

Task2 additional member (blended at weight 0.3, not full 1.0 — see below):
```
runs/task2_seed202/fold3/final.pth
```

Task3 source (5-fold only, NOT the 11-fold ensemble):
```
runs/task1/fold{0..4}/final.pth   # seed=77 only
```

## Durable checkpoint backup

12 checkpoint files each (24 total) are archived as **public** Kaggle
Datasets, not just on the local training machine — confirmed public
2026-08-07 (`isPrivate` cleared via `kaggle datasets metadata --update`,
both were private by default until then, since they were originally
uploaded only for this account's own Kaggle-kernel use, not for review):

- Task1: `aaronajit/gave2-task1-7fold-ckpts` (`fold0..fold11_final.pth`)
- Task2: `aaronajit/gave2-task2-7fold-ckpts` (`fold0..fold11_final.pth`)

`fold0..fold10` are the 11-fold base (seed77 folds0-4, seed101 folds0-4,
seed202 fold0); `fold11` is the seed202/fold3 checkpoint used at 0.3 weight.
Task1's `fold11` is included for completeness (it was the warm-start basis
for Task2's `fold11`) even though it isn't itself used in the submitted
Task1 ensemble — so the *submitted* recipe uses 11 Task1 checkpoints + 12
Task2 checkpoints, not 12 of each. The `-7fold-` in both dataset names is a
stale label from an earlier, smaller ensemble size; left unchanged to avoid
breaking the existing dataset URLs (referenced from the report and here).

## Commands

### 1. Train each fold
```bash
python src/train_task1.py --data-root data/raw/GAVE2_preliminary --fold N --n-folds 5 \
  --patch-size 384 --base-ch 64 --iterations 5 --epochs 60 --steps-per-epoch 50 \
  --batch-size 1 --lr 0.0001 --num-workers 2 --amp-dtype bf16 --pos-weight 5.0 \
  --cldice-weight 0.3 --vein-pos-weight 6.0 --vein-topology-ratio 1.3 \
  --out-dir runs/task1[_altseed|_seed202] --checkpoint-every-epochs 5 --val-every-epochs 5 \
  --seed [77|101|202]

python src/train_task2.py --data-root data/raw/GAVE2_preliminary --ffa-root data/registered \
  --fold N --n-folds 5 --patch-size 320 --base-ch 64 --iterations 5 --epochs 60 \
  --steps-per-epoch 50 --batch-size 1 --lr 0.0001 --num-workers 2 --amp-dtype bf16 \
  --warm-start-task1 runs/task1.../foldN/final.pth --pos-weight 5.0 --vein-pos-weight 6.0 \
  --cldice-weight 0.3 --vein-topology-ratio 1.3 --out-dir runs/task2[_altseed|_seed202] \
  --checkpoint-every-epochs 5 --val-every-epochs 5 --seed [77|101|202] --fusion additive
```

### 2. Task1 inference (11-fold ensemble + TTA)
```bash
python src/predict_ensemble.py --task task1 --tta \
  --checkpoints <11 Task1 checkpoints listed above> \
  --images-dir data/raw/GAVE2_preliminary/validation/images \
  --masks-dir data/raw/GAVE2_preliminary/validation/masks \
  --out-dir predictions/task1/validation
```

### 3. Task2 inference (11-fold ensemble + TTA, then blend in fold3 at weight 0.3)
```bash
python src/predict_ensemble.py --task task2 --tta \
  --checkpoints <11 Task2 checkpoints listed above> \
  --images-dir data/raw/GAVE2_preliminary/validation/images \
  --masks-dir data/raw/GAVE2_preliminary/validation/masks \
  --ffa-dir data/registered/validation \
  --out-dir predictions/task2_11fold/validation

python src/predict_ensemble.py --task task2 --tta \
  --checkpoints runs/task2_seed202/fold3/final.pth \
  --images-dir data/raw/GAVE2_preliminary/validation/images \
  --masks-dir data/raw/GAVE2_preliminary/validation/masks \
  --ffa-dir data/registered/validation \
  --out-dir predictions/task2_fold3_new/validation

# weighted pixel-level merge: combined = (11*11fold_avg + 0.3*fold3) / 11.3
python merge_weighted.py predictions/task2_11fold/validation predictions/task2_fold3_new/validation \
  predictions/task2_final/validation 11 0.3
```

### 4. Task1 inference for Task3 sourcing (5-fold only, separate from step 2)
```bash
python src/predict_ensemble.py --task task1 --tta \
  --checkpoints runs/task1/fold{0..4}/final.pth \
  --images-dir data/raw/GAVE2_preliminary/validation/images \
  --masks-dir data/raw/GAVE2_preliminary/validation/masks \
  --out-dir predictions/task1_5fold/validation
```

### 5. Task3 biomarker computation
```bash
python src/run_task3.py \
  --av-dir predictions/task1_5fold/validation \
  --images-dir data/raw/GAVE2_preliminary/validation/images \
  --masks-dir data/raw/GAVE2_preliminary/validation/masks \
  --threshold 140 \
  --out-dir predictions/task3/validation
```

### 6. Package
```bash
python src/format_submission.py --team-id aaronteam \
  --task1-dir predictions/task1/validation \
  --task2-dir predictions/task2_final/validation \
  --task3-dir predictions/task3/validation \
  --out-zip submissions/final.zip
```

`merge_weighted.py` (referenced in step 3) is included at the repo root of this archive
under `tools/merge_weighted.py` — it wasn't part of the original `src/` tree since it
was written as a one-off during the final ensembling experiments.

## Key findings that shaped this recipe (see submissions_log.csv for full detail)

- Task3 should be sourced from a **smaller (5-fold), not larger** ensemble than
  Task1/Task2 — larger ensembles blur thin vessel structure, hurting fractal-dimension
  and caliber-sensitive biomarkers even as they help Task1/Task2's pixel/topology metrics.
  Tested at 2-fold, 5-fold, 8-fold, 11-fold sources; 5-fold won clearly.
- Task3 binarization threshold=140 (~0.55) beats the default 127 and also beats 153;
  per-channel (R/G/B) threshold splitting was tried and made things worse — likely
  distorts the top-6-widest-vessel caliber measurement (CRAE) even when density/fractal
  metrics look fine.
- New ensemble members should NOT be added at full/equal weight without validating
  first — two folds (seed202 fold2 full-weight, fold3 full-weight) both regressed the
  ensemble; the same fold3 checkpoint at 0.3 weight instead was a net positive.
- Cross-attention fusion (`src/models/cmrrwnet_xattn.py`) and self-training/pseudo-labeling
  were both tried and rejected with real leakage-free validation evidence (see log).
