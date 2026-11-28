# Lean check of the four-vertex recursion

At freezing rate 1/1000 on the four-vertex complete graph, Lean recomputes three probabilities in the embedded jump chain and proves their covariance expression is strictly negative. The edge order is 01, 02, 03, 12, 13, 23. The masks 33 and 30 represent the matching and its complement. The recursion starts with all edges closed and all vertices warm, gives weight 1000 to each eligible edge opening and weight 1 to each warm-component freeze, and stops when further openings are impossible or the specified class has already opened. The three equalities returning a probability certify that their recursions finish within the depth bound. The paper identifies this jump chain with the continuous-time process, identifies the expression with covariance of the increasing events, and proves the interval and all-rate results.

The file imports only `Std` from Lean 4.30.0. Replay from this directory with the pinned toolchain.

```sh
lean -DwarningAsError=true FreezingWitness.lean > actual-axioms.txt
diff -u expected-axioms.txt actual-axioms.txt
```

The workflow runs the Lean kernel and checks the printed axiom report.
