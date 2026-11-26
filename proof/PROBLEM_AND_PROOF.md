# Problem and proof

The model starts with all vertices warm and edges closed. A closed edge with warm endpoints opens at rate 1. Each connected warm component of the open-edge graph freezes at rate α. A freeze preserves its open edges and permanently blocks unopened edges incident to its vertices.

On $K_4$, let $M=\{01,23\}$ and $C=E(K_4)\setminus M$. Let $A$ and $B$ be the increasing events that some edge of $M$ and some edge of $C$ open, respectively. Let $p_M$ and $p_C$ be the probabilities of missing their respective edge classes and let $p_0$ be the probability that no edge opens. The covariance is $p_0-p_Mp_C$.

1. No opening requires three consecutive singleton freezes, giving $p_0=4\alpha^3/[(1+\alpha)(1+2\alpha)(3+2\alpha)]$.
2. One cross edge opens and its newly joined pair freezes. This blocks both matching edges and gives $p_M\geq [4/(6+4\alpha)][\alpha/(5+3\alpha)]$.
3. Both matching edges open first and then either resulting pair freezes. This blocks all four cross edges and gives $p_C\geq[2/(6+4\alpha)][1/(5+3\alpha)][2\alpha/(4+2\alpha)]$.

For $0<\alpha\leq1/1000$, these give $p_0<\alpha^2/750<4\alpha^2/2205<p_Mp_C$. The [paper](../paper/manuscript.pdf) also proves the degree bound behind an exact calculation of the sign at every positive rate for this pair.
