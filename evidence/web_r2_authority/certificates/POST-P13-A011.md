# POST-P13-A011 — W09-SE002 and W09-SE003

Critical-layer certificate. The frozen 78-page P13R diplomatic edition is immutable.

**Status:** repaired

**Theorem (intersection/index).** Let $L/K$ be the original splitting field, $M=K(r)$ an auxiliary extension, $E=L\cap M$, $G=\operatorname{Gal}(L/K)$, and $H=\operatorname{Gal}(L/E)$. Then $[G:H]=[E:K]$ and $[E:K]\mid[M:K]$.

**Proof.** The Galois correspondence gives $[G:H]=[E:K]$. Since $E$ is a subfield of $M$, the tower law gives $[M:K]=[M:E][E:K]$. If $[M:K]=p$ is prime, the index is $1$ or $p$. Without prime degree the dichotomy is false: $r=\sqrt2+\sqrt3$ has degree $4$, contains $\mathbf Q(\sqrt2)$, and reduces its $C_2$ splitting group with index $2$.

**Theorem (Proposition III normality).** If $M/K$ is also a splitting field, then $E/K$ is finite Galois, so $H$ is normal in $G$. Consequently the subgroups arising from conjugate auxiliary roots coincide after all auxiliary roots are adjoined.

**Propagation.** These two theorems replace the undefined p and the omitted proof. They control all dependent group decompositions and the subsequent radical tower.
