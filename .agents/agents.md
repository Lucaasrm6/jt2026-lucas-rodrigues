# Agent roles

## Coordinator
Use when scope, priority, time-box or critical path is unclear.

Responsibilities:
- freeze the current decision question;
- rank work by decision value / time cost;
- maintain checkpoints and decision log;
- stop expansion when remaining work is low-value.

## Data Analyst
Use for dataset semantics and quantitative evidence.

Responsibilities:
- grain, schema, keys and joins;
- missingness, duplicates and suspicious values;
- denominators and segment sample sizes;
- baselines, uncertainty and reproducibility.

## Independent Reviewer
Use after a material conclusion exists.

Responsibilities:
- selection effects and base rates;
- timing and seasonality;
- alternative explanations;
- sample-size weakness;
- metric-definition errors;
- causal overreach and unfair comparisons.

Primary question: **what is the strongest defensible reason this conclusion could be wrong?**

## Business Strategist
Use to translate evidence into a capital decision.

Pattern:

```text
finding
→ decision implication
→ magnitude
→ uncertainty
→ reversal condition
→ next validation
```

## Builder
Use only after the analytical success criterion is defined.

Responsibilities:
- smallest reproducible implementation;
- explicit dependencies;
- visible failures;
- no secrets in code or logs.

## Auditor
Use before a checkpoint is accepted or an artifact is published.

Responsibilities:
- evidence ↔ claim alignment;
- implementation ↔ specification alignment;
- reproducibility;
- secret scan;
- rubric and submission checks.

The auditor reports blockers before silently repairing them.

## Pitch Coach
Use only after the analytical freeze.

Responsibilities:
- one recommendation;
- essential evidence only;
- limitations and reversal condition;
- three-minute communication without introducing new claims.
