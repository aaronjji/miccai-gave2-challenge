# GAVE2 Finals Verification — Submission Checklist

Deadline: **August 9, 23:59 Beijing time**, to `pengqiyu2004@163.com`, CC `omia@hdmilab.cn`.

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

## 4. Not yet done — flag if you want it

- DockerHub image (optional per the email, not built)
- Actually rendering the report PDF (needs Overleaf or a LaTeX install —
  see main reply)
