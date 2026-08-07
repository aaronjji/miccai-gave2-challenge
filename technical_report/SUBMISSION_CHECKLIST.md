# GAVE2 Finals Verification — Submission Checklist

Deadline: **August 9, 23:59 Beijing time**, to `pengqiyu2004@163.com`, CC `omia@hdmilab.cn`.

## 0. Primary contact designation (NEW, Aug 1 reminder — send ASAP, separate from everything else)

Per the Aug 1 reminder email: all top-30 teams must designate a primary
email contact. Send to `pengqiyu2004@163.com`:

> Team name: aaronteam
> Primary contact email: aaronaajit@gmail.com

This is distinct from the confirmation reply and the material submission —
send it as its own email, promptly.

## 1. Confirmation reply (send this first, separately)

Reply to the original email with exactly this (per their instruction — one
team member only, and all future correspondence should come from the same
person):

> Confirmation received.

Sent from Aaron's email so all follow-up correspondence is consistent with
"one contact person."

## 2. Verification materials zip (by Aug 9)

Rename the zip with your team name before sending, e.g. `aaronteam.zip`.
Contents:

- [ ] **Technical report PDF** — compile `technical_report/gave2_report.tex`
      (see compile instructions in the main reply). Double check the
      rendered PDF: title/author/affiliation correct, Fig. 1 diagram
      readable, references render correctly.
- [ ] **Preliminary submission results** — the report references round score
      7.06756; attach/include supporting evidence if they want it separately
      (e.g. a screenshot or export of your submission history —
      `submissions_log.csv` in the repo already has the full log, but the
      email says "preliminary submission results" as a distinct deliverable,
      so consider also including a leaderboard screenshot showing your final
      rank and score).
- [ ] **Code**: GitHub link is already in the report
      (`https://github.com/aaronjji/miccai-gave2-challenge`, now public). No DockerHub
      image currently exists — the email recommends but doesn't strictly
      require both; GitHub alone should satisfy requirement (11). If you
      want a DockerHub image too, that's separate follow-up work (needs a
      Dockerfile + a DockerHub account/push) — let me know if you want that.

## 3. Things only you can do (not automatable)

- [ ] At least one team member (you) must register for the **October 1
      OMIA Workshop** at MICCAI 2026 and complete payment:
      https://conferences.miccai.org/2026/en/REGISTRATION.html — needed
      **only if** you're confirmed as a finalist (top 15 after material
      review), but worth knowing about now given the timeline.
- [ ] Re-read the "same model" rule before finals: *"The model used in the
      finals must be the same as the one corresponding to your final
      preliminary results; replacement with a new model is not allowed."*
      This matches what's now archived in `STANDING_BEST_RECIPE.md` — don't
      train a new/different model between now and the finals blind test
      (opens ~Sept 5) even if you're tempted to keep improving; that would
      risk disqualification.

## Context worth knowing

- **External pretrained weights are fine.** Read the full official rules
  page (Aug 1) — no restriction anywhere on using pretrained weights/models.
  The only related clause (Supplement 3) prohibits submitting the baseline's
  *predictions* unchanged, not building on pretrained components, which is
  what this pipeline does (HRF-pretrained RRWNet, REFUGE-pretrained
  SegFormer) — already disclosed in the report regardless.
- **Final scoring**: `Score_total = 0.3 × Score_preliminary + 0.7 × Score_final`.
  The preliminary result (round=7.06756) is locked in as 30% of the overall
  outcome no matter what happens in finals — not just a qualifying gate.
- Rule (11): top teams may be invited to co-author a joint journal
  paper (max 2 authors/team) summarizing methods/results across the
  challenge. Not actionable now, just worth knowing if you place well.
- Rule (12): official WeChat group exists for challenge communication
  (format "Team ID - Name" after joining); non-Chinese-speaking
  participants can stick to `omia@hdmilab.cn` instead.

## 4. Not yet done — flag if you want it

- DockerHub image (optional per the email, not built)
- Actually rendering the report PDF (needs Overleaf or a LaTeX install —
  see main reply)
