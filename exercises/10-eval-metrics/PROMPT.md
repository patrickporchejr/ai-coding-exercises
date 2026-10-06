# Exercise 10: Compute Eval Metrics from Labeled Data

**Skills:** metrics from scratch, handling label disagreement. This ties directly to the eval track (exercises 1–3).

## The interview prompt

> We ran a support-ticket classifier on 300 tickets, and two human annotators labeled the same tickets independently. The data is in `labels.csv`. The annotators don't always agree.
>
> Compute accuracy, precision, recall, and F1 per class. Measure how much the annotators agree with each other, and show where the model and the humans disagree most.

## Input

`labels.csv` has these columns: `id`, `text`, `model_label`, `annotator_a`, `annotator_b`.

The classes are `billing`, `bug`, `feature_request`, `account`, `other`. Look closely at the label columns before computing anything.

## Deliverables
1. **Metrics written from scratch**, without sklearn: accuracy, plus per-class precision, recall and F1, then macro and weighted averages. You may use sklearn *afterwards* to check your numbers.
2. **A decision about ground truth.** There's no "true label" column. Decide what counts as gold (annotator A? B? only rows where they agree? something else?) and show how the model's scores change under at least two choices.
3. **Annotator agreement**: raw percent agreement and **Cohen's kappa**, also computed from scratch. Explain why kappa is lower than raw agreement.
4. **Confusion matrices**: model vs. your gold, and annotator A vs. annotator B. Name the top 3 confusions and show example tickets for each.
5. **A short recommendation**: is the model's weakness in the model, in the labels, or in the class definitions?

## Debrief questions
- How did you handle blank labels and inconsistent label spellings? How did that choice move the numbers?
- When would you report macro F1 instead of accuracy?
- The annotators agree about 80% of the time. What does that mean for how high the model's score can meaningfully go?
- How would you fix the labeling process, not just the model?
