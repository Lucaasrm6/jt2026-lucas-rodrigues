# /final-audit

Objetivo: separar validade analítica de readiness da entrega.

```text
1. Reproduce decisive numbers from source data.
2. Compare implementation against written definitions.
3. Review claims for unsupported causal/business language.
4. Run critical decision tests.
5. Run the executable Consistency Gate.
6. If any check fails: BLOCK the freeze and patch only the affected issues.
7. Verify README, AI log, video requirements and public-access requirements.
8. Release only after all blocking checks pass.
```

A verification gate must be able to fail. A hard-coded PASS is not a gate.
