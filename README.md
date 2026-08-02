# GAVE2 (MICCAI 2026 OMIA Workshop Challenge) — Team aaronteam

Solution for the **GAVE2** challenge (Generalized Analysis of Vessels in Eye,
Edition 2), part of the OMIA workshop at **MICCAI 2026**
([challenge page](https://aistudio.baidu.com/competition/detail/1463/0/introduction)).
Team **aaronteam** (Aaron Ajit) — preliminary round round score **7.06756**,
top 30 finish, advancing to the finals verification stage.

Three tasks on color fundus photos (CFP): (1) artery/vein segmentation from CFP alone,
(2) cross-modal AV segmentation with paired early/late-phase FFA, (3) vascular
biomarker quantification (AVR, vessel density, fractal dimension) from the
predicted segmentation.

Built on the official GAVE2 baseline, [CMRRWNet](external/cmrrwnet), and its
[RRWNet](external/rrwnet) backbone (Morano et al., *Expert Systems with
Applications* 2024), with a topology-aware soft-clDice loss, a multi-seed
cross-validation ensemble, and a corrected/tuned Task 3 biomarker-sourcing
pipeline. Full technical report: [`technical_report/gave2_report.tex`](technical_report/gave2_report.tex).
Exact commands + checkpoints to reproduce the final submission:
[`STANDING_BEST_RECIPE.md`](STANDING_BEST_RECIPE.md). Full experiment history
(what was tried, what worked, what didn't, and why): [`submissions_log.csv`](submissions_log.csv).

## Layout

- `external/` — git submodules: `rrwnet` (baseline architecture, pretrained weights),
  `cmrrwnet` (reference baseline architecture), `mnet_deepcdr` (optic disc
  localization), `minima` (CFP/FFA registration).
- `configs/` — training configs (YAML), one per task/fold variant.
- `src/datasets/` — shared Dataset classes for Task 1 (CFP-only) and Task 2 (CFP+FFA).
- `src/models/` — RRWNet, baseline-equivalent 5ch fusion, and improved fusion models.
- `src/losses/` — Dice/BCE + soft-clDice (topology-aware).
- `src/metrics/` — local reimplementation of the official scoring formulas (pixel +
  topology metrics for Task 1/2, MAE/SMAPE for Task 3) — build and calibrate this
  BEFORE trusting any local model comparison.
- `src/biomarkers/` — SIVA zone geometry, Knudtson CRAE/CRVE/AVR, density, fractal
  dimension (Task 3).
- `src/od_localization/` — optic disc detection (required for Task 3 zones; not
  provided in the dataset).
- `src/registration/` — MINIMA-based CFP/FFA registration (required for Task 2; pairs
  are not pre-registered).
- `data/` — not tracked in git. Download per `scripts/00_download_and_inspect.py`
  instructions; do not re-host (dataset usage terms).
- `notebooks/validate_metrics_against_baseline.ipynb` — reproduce the reference
  baseline's published scores locally before trusting any of this repo's own
  experiments.
- `notebooks/validate_biomarkers_against_gt.ipynb` — reproduce provided GT biomarker
  labels from GT masks before ever running Task 3 on predicted masks.
- `submissions_log.csv` — every real leaderboard submission: date, task, config hash,
  local score, leaderboard score. Submission window closes 2026-07-31 23:59, capped
  at 5 submissions/day — don't burn slots on unvalidated experiments.

## Setup

```bash
conda env create -f environment.yml
conda activate gave2
git submodule update --init --recursive
```
