# TakeMeter

> ### ⚠️ Partial submission — resubmitting for a higher grade
>
> Updated at the unit 6 deadline. **Unit 5 is now fully done:** community,
> label taxonomy, all five acceptance criteria, the full `labels.csv` (202
> posts), the real training run (`results.json`, `test_split.csv`), and every
> unit 5 README section. **Unit 6 still to come:** the baseline comparison,
> three-seed retrain, confusion matrix, agreement report (blocked on
> `data/staff_labels.csv`, which has to come from my TF), verdicts/diagnoses,
> and one improvement with a re-run. I'll resubmit the same repository URL
> once those are complete.

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

This classifier reads posts from **r/nba**, the main NBA subreddit, and sorts
each one into one of three categories: `hot_take`, `analysis`, or `reaction`.
r/nba is dominated by exactly these three modes of talking about basketball —
confident unsupported claims about players and teams, arguments that cite a
specific stat or fact, and in-the-moment responses to live games, trades, and
news. TakeMeter exists to tell them apart automatically, which is the first
step toward surfacing the posts that actually make an argument instead of
just asserting one.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `hot_take`

**Definition:** A confident claim about a player's, team's, or play's quality,
ranking, or future, offered with no supporting evidence.

**Example 1:**
> "Wemby is already a better defender than Rudy Gobert."

**Example 2:**
> "The Celtics are not winning another title with this core."

### `analysis`

**Definition:** An argument about a player, team, or game that is backed by a
specific, checkable stat or fact.

**Example 1:**
> "Harden's turnover rate is actually down 3% since the trade, and his true
> shooting against drop coverage is the best it's been in four years."

**Example 2:**
> "The Nuggets are 14-2 this season when Jokic has fewer than 4 turnovers —
> that's the real swing stat for them, not his scoring."

### `reaction`

**Definition:** An immediate response to something that just happened in a
game, trade, or news event, not yet developed into a broader claim.

**Example 1:**
> "NOOOO HE AIRBALLED THE GAME WINNER"

**Example 2:**
> "Wait, they actually traded him?? I did not see that coming."

### The hardest boundary

**Which two labels:** `hot_take` and `analysis`

**The decision rule I used every time:**
If the post cites a specific, checkable stat or fact to support its claim,
it's `analysis` — even if the overall tone is heated or the conclusion is
debatable. If the claim is asserted with confidence but backed only by vibes,
unnumbered comparisons, or "everyone knows," it's `hot_take`. A secondary rule
for `reaction` vs. `hot_take`: if the post is describing or responding to
something that just happened without generalizing into a claim about a
player's or team's quality or ranking, it's `reaction`. The moment it
generalizes into that kind of claim, it's `hot_take`, even if a live event
triggered it.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/nba. Reddit's API is no longer accepting new
developer registrations (closed to new applicants as of Oct 31, 2026), so
posts were collected by browsing r/nba directly — hot and top listings,
individual game threads, and comment sections of debate-style posts (e.g. a
"most overrated all-time great" thread) — and reading them off screenshots.

**How I labelled them:** 20 posts were labelled cold — read and labelled by
me with no AI suggestion visible before I committed to a label. The remaining
182 were pre-labelled by Claude against the exact definitions and decision
rule in this README, then I read and either confirmed or corrected every
single one individually (1 label was corrected on review). Posts flagged as
"borderline" by the pre-labelling pass were reviewed first and most
carefully, since those were the likely error cases.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| reaction | 104 | 51.5% |
| hot_take | 50 | 24.8% |
| analysis | 48 | 23.8% |
| **Total** | 202 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "The Kings have no interest in keeping Sabonis, and he is not
> enthused about playing with a ball-dominant guard like Acuff. But getting a
> first-rounder for him would be a major score, and a longshot."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* I labelled this `hot_take`. It names a specific
> situation (the Acuff fit) the way `analysis` posts do, but nothing in it is
> actually a checkable fact — "not enthused" and "a major score" are the
> poster's own read on the situation, not a stat or a reported quote. My rule
> says a claim only earns `analysis` if it cites something verifiable; naming
> a real player isn't the same as citing a real number.

**2.**
> *The post:* "The Sacramento Kings are the last winless team in the NBA"
>
> *Could have been:* `reaction` or `analysis`
>
> *I chose, because:* I labelled this `analysis`. It reads like a bare
> reaction at first, but it's actually a checkable, specific claim about
> where a team stands relative to the entire league, not just a description
> of something that just happened in a game. That distinction — a verifiable
> claim about standing vs. a play-by-play recap — is what pushed me to
> `analysis` even though there's no "argument" sentence attached to it.

**3.**
> *The post:* "A little biased? Duncan is arguably the greatest PF, but he
> didn't do enough to be in the GOAT discussion. Kobe's in the same boat.
> He's 2nd greatest SG of all, and came up short. Both have 5. Both were
> considered the best, and one of the best players in the league at their
> peaks."
>
> *Could have been:* `analysis` or `hot_take`
>
> *I chose, because:* I labelled this `hot_take`, overriding my own
> pre-labelling pass. "Both have 5" (rings) is a real, checkable fact, which
> is the kind of thing my decision rule says should earn `analysis`. But that
> one fact is buried in a post that's otherwise pure ranking opinion ("2nd
> greatest SG", "didn't do enough") — the rings aren't being used to support
> a specific argument, they're decoration on a take that was already made.
> This is the clearest case where my decision rule needs a tiebreaker: one
> real stat doesn't make a post `analysis` if the stat isn't doing the actual
> argumentative work.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42 — all
defaults, unchanged.

**Anything I changed from the defaults, and why:** Nothing. This is the
first training run, meant to establish a baseline before any tuning.

**Split sizes:** 140 train / 31 val / 31 test (70/15/15 of 202 total).
Per-label counts in the test split: `reaction` 16, `hot_take` 8, `analysis`
7. Both `hot_take` and `analysis` are right at or below the ~8-example
threshold the brief warns about — their F1 scores should be read as noisy,
not stable, until the three-seed run in unit 6.

**Device:** `mps` (Apple Silicon GPU), torch 2.15.0.

**Unit 5 result:** accuracy 0.581, macro F1 0.385. Per-label F1: `analysis`
0.444 (n=7), `hot_take` 0.000 (n=8), `reaction` 0.711 (n=16). The confusion
matrix shows every `hot_take` test example was predicted as `reaction` —
the model collapsed toward the majority label rather than learning the
`hot_take` boundary at all. This is a real, single-seed result; unit 6's
three-seed run will show whether it's representative or if seed 42
specifically was unlucky with such a thin `hot_take` test split.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I sent Claude screenshots of r/nba (hot/top listings
  and comment threads) since I couldn't scrape or API-access Reddit
  (self-service API registration is closed to new applicants as of Oct 31,
  2026), and asked it to read out real post/comment text and pre-label each
  one against the three definitions and the hot_take/analysis decision rule
  in this README.
- *What came back:* A working CSV of candidate posts, each with an AI-chosen
  label and a confidence flag ("clear" vs. "borderline"), skipping anything
  too thin to label (bare clip captions, meta/trivia posts with no real
  argument).
- *What I changed:* I read every single row and either confirmed or
  corrected the label — the "borderline"-flagged ones got the closest look.
  One label was changed outright (the Duncan/Kobe comparison, hard case #3
  above), and I separately hand-labelled 20 posts cold, without seeing the
  AI's suggested label first, per the note column.

**Moment 2**

- *What I asked for:* I asked Claude to build a review spreadsheet
  (`data/review_this.csv`) I could edit directly on github.com, with mostly
  blank columns so I'd only have to touch what I wanted to change rather than
  re-type every row.
- *What came back:* A simplified CSV with `your_label`, `cold`, and
  `exclude` columns. I used it to mark my 20 cold labels, flag 3 near-
  duplicate posts (two Reddit threads independently posting about the same
  Victor Wembanyama 43-point game) for exclusion, and override one label.
- *What I changed:* I caught and corrected an off-by-one indexing error in
  which rows got excluded (Claude had excluded ids 90/119/126 when I'd meant
  91/120/127) by checking the actual post text against what I intended to
  exclude, not just trusting the row numbers.

**Pre-labelling disclosure:** Yes — 182 of 202 final labels started as a
Claude pre-label that I individually reviewed and either confirmed or
corrected, as described above. 20 were labelled by me with no AI suggestion
visible beforehand (`note: cold` in labels.csv).

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.710 | 0.581 | -0.129 |
| Macro F1 | 0.515 | 0.385 | -0.130 |
| F1 — `analysis` | 0.632 | 0.444 | -0.188 |
| F1 — `hot_take` | 0.000 | 0.000 | 0.000 |
| F1 — `reaction` | 0.914 | 0.711 | -0.203 |

**What I predicted before I looked:** I can't honestly fill this in as a
blind prediction. Time pressure meant I ran the unit 5 training (and wrote up
its results) *before* running the baseline, which is the reverse of the
order this section assumes — so by the time I ran `baseline.py` I already
knew the trained model's numbers. Disclosing that rather than writing a fake
"prediction" after the fact.

**What the gap actually means:** The baseline — a general-purpose zero-shot
model with no training, just my label definitions as a prompt — beat my
fine-tuned model on every measure. That's a real finding, not a failure to
report quietly: with only 140 training examples and 3 epochs, the fine-tune
likely didn't have enough signal to beat a strong pretrained model that
already has broad language understanding baked in. Both models still failed
identically on `hot_take` (F1 0.000) — that label is hard for a reason that
has nothing to do with fine-tuning, which points at either the label
definition itself or the examples, not the training process.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
