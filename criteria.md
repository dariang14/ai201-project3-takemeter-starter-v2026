# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy of at least 0.65 on the held-out test set.

**Why this target:** With three labels, a coin-flip guesser clears about 33%,
so 0.65 requires real signal, not luck. I'm not setting it higher than that
because the hardest boundary in my taxonomy (`hot_take` vs. `analysis`) is
genuinely fuzzy even for a human reader — I expect some of that confusion to
survive into the model, and 0.65 leaves room for it while still ruling out a
model that's just guessing the majority label.

---

## 2. Macro F1 of at least 0.60 across all three labels.

**Why this target:** Overall accuracy alone can be flattered by one easy,
overrepresented label. Macro F1 averages the three labels equally, so the
model can't hit its target by nailing `reaction` (which I expect to be the
easiest to spot — all-caps, exclamation points, present tense) while ignoring
the other two.

---

## 3. F1 for `reaction` of at least 0.50.

**Why this target:** This is my smallest and noisiest label by design — I'm
aiming for roughly a third of 200 examples per label, so `reaction` will land
around 60-65 examples, which means roughly 9-10 in the test split. A score
computed on 9-10 examples swings a lot between seeds, so I'm giving it a
looser target than my overall accuracy rather than pretending it'll be as
stable as the full-set number.

---

## 4. No single label makes up more than 65% of my 200 labeled examples.

**Why this target:** The brief's floor is 70%, but I'm setting my own target
tighter because my taxonomy only has three labels — if one label dominates
even within the 70% cap, the other two split a small remainder and both end
up too thin to measure reliably. 65% still leaves room for r/nba's natural
skew (hot takes and reactions are more common than stat-backed analysis)
without letting one label swallow the dataset.

---

## 5. Of the predictions the model makes with at least 0.80 softmax
confidence, at least 85% should be correct.

**Why this target:** A "take meter" is only useful if a confident prediction
can be trusted — a model that's 65% accurate overall but equally overconfident
on its wrong answers is worse than one that knows when it's unsure. Because
`hot_take` and `analysis` share a fuzzy boundary, I expect genuine uncertainty
on some posts, and I'd rather the model express that uncertainty than guess
confidently and be wrong.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
