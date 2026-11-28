# Status

[Version 1.0.0](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/releases/tag/v1.0.0) · 27 November 2026 · [Version DOI](https://doi.org/10.5281/zenodo.24567309)

The three-history proof answers Mottram’s finite positive-association question. The all-rate threshold concerns only the specified event pair. Mottram’s earlier four-vertex path fails the stronger FKG lattice condition and has positive association.

Internal mathematical review covered the stated result and its scope. External peer review has not been conducted. The replay verifies exact equality at the 63 rational nodes specified by the degree bound, the sign bracket, and the thesis’s path-law calibration.

The repository verification, replay and PDF build workflows succeeded on the [reviewed commit](https://github.com/DannyExperiments/constant-freezing-percolation-counterexample/commit/700592fafefc6311bf17d56bab4eac8ca7d60fa2). See the [literature and priority audit](audits/public_safe_reports/LITERATURE_AUDIT.md).

The current main branch adds [a scoped Lean certificate](formalization/README.md). At freezing rate 1/1000 on the four-vertex complete graph, Lean recomputes three probabilities in the embedded jump chain and proves their covariance expression is strictly negative. The edge order is 01, 02, 03, 12, 13, 23. The masks 33 and 30 represent the matching and its complement. The recursion starts with all edges closed and all vertices warm, gives weight 1000 to each eligible edge opening and weight 1 to each warm-component freeze, and stops when further openings are impossible or the specified class has already opened. The three equalities returning a probability certify that their recursions finish within the depth bound. The paper identifies this jump chain with the continuous-time process, identifies the expression with covariance of the increasing events, and proves the interval and all-rate results.
