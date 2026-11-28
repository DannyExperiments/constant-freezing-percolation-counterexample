# Claims and evidence

| Claim | Evidence |
|---|---|
| Mottram asked about positive association | Thesis §3.1.4, checked against the canonical Cambridge PDF |
| Counterexample on $K_4$ for $0<\alpha\leq 1/1000$ | Three jump histories and explicit inequalities, manuscript Theorem 1 |
| Covariance sign for the stated events at every positive rate | Manuscript Proposition 2, cleared difference degree ≤62, exact equality at 63 distinct rational inputs |
| Unique positive root and location | Positive nonconstant coefficients, negative constant term, and exact endpoint sign checks |
| Agreement with Mottram’s path law at $\alpha=1$ | All eight final masses and the lattice defect, [replay output](verification/logs/replay.txt) |
| Illustrated jump factors and event outcomes | Fixture checks against eligible edges, warm components and the exact terminal law in [renderer](visualization/render.py) |

## Partial Lean evidence

At freezing rate 1/1000 on the four-vertex complete graph, Lean recomputes three probabilities in the embedded jump chain and proves their covariance expression is strictly negative. The edge order is 01, 02, 03, 12, 13, 23. The masks 33 and 30 represent the matching and its complement. The recursion starts with all edges closed and all vertices warm, gives weight 1000 to each eligible edge opening and weight 1 to each warm-component freeze, and stops when further openings are impossible or the specified class has already opened. The three equalities returning a probability certify that their recursions finish within the depth bound. The paper identifies this jump chain with the continuous-time process, identifies the expression with covariance of the increasing events, and proves the interval and all-rate results. [Kernel-checked source](formalization/FreezingWitness.lean)
