# A finite counterexample to positive association for constant-freezing percolation

[![Repository verification](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/verify.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/verify.yml) [![Replay verification](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/replay.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/replay.yml) [![PDF build](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/pdf.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/pdf.yml)
[![Partial Lean verification](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/lean.yml/badge.svg?branch=main)](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/actions/workflows/lean.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24567309.svg)](https://doi.org/10.5281/zenodo.24567309)

Mottram asked whether the final open-edge law of percolation with constant freezing is positively associated. On $K_4$, let $A$ be the event that a fixed perfect matching has an open edge and let $B$ be the event that its complement has an open edge. Both events are increasing. Their covariance is strictly negative for every $0<\alpha\leq 1/1000$.

[Read the paper (PDF)](paper/manuscript.pdf) · [Proof at a glance](proof/PROBLEM_AND_PROOF.md) · [Exact replay](REPRODUCIBILITY.md)

## Watch the three histories

![A rotating tetrahedron shows three constant-freezing histories. The empty outcome needs three freezes. Each of the two edge classes can be missed after one freeze.](visualization/freezing-histories.gif)

[Download the offline explorer](https://raw.githubusercontent.com/DannyExperiments/constant-freezing-percolation-counterexample/3677d24af75d4f415dbb2e8763aa8df347de4c90/visualization/freezing-histories-explorer.zip), extract it, and open `index.html` in a browser. Rotate the tetrahedron and step through each history to see its exact jump factors.

The elementary proof starts from three histories of the four labeled vertices. A separate exact certificate gives the sign for these two events at every positive rate. The covariance crosses zero at a unique rate between 0.0407722920 and 0.0407722921. The crossing only concerns these two events.

## Sources and checks

- [Mottram’s thesis, §3.1.4 and Example 3.1.5](https://doi.org/10.17863/CAM.15980)
- [Literature audit](audits/public_safe_reports/LITERATURE_AUDIT.md)
- [Mathematical audit](audits/public_safe_reports/MATHEMATICAL_AUDIT.md)
- [Scope and limitations](CLAIM_SCOPE_AND_LIMITATIONS.md)
- [Provenance](PROVENANCE.md) and [AI credits](AI_DISCLOSURE.md)

Internal mathematical review is complete. See the [release and verification status](STATUS.md).

[Release v1.0.0](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/releases/tag/v1.0.0) · [Version DOI](https://doi.org/10.5281/zenodo.24567309)

## Partial Lean verification

At freezing rate 1/1000 on the four-vertex complete graph, Lean recomputes three probabilities in the embedded jump chain and proves their covariance expression is strictly negative. The edge order is 01, 02, 03, 12, 13, 23. The masks 33 and 30 represent the matching and its complement. The recursion starts with all edges closed and all vertices warm, gives weight 1000 to each eligible edge opening and weight 1 to each warm-component freeze, and stops when further openings are impossible or the specified class has already opened. The three equalities returning a probability certify that their recursions finish within the depth bound. The paper identifies this jump chain with the continuous-time process, identifies the expression with covariance of the increasing events, and proves the interval and all-rate results. [Lean source](formalization/FreezingWitness.lean) · [Replay and scope](formalization/README.md)
