# POST-P13-A005 — PDF051 converse and the degree-9/25 exceptions

Critical-layer certificate. The frozen 78-page P13R diplomatic edition is immutable.

**Status:** rejected

**Theorem.** The printed claim that the only exceptional solvable primitive degrees outside the one-dimensional semilinear form are 9 and 25 is false.

**Counterexample.** Let W=F_2^2 and V=W⊕W. Let A=[[0,1],[1,1]] of order 3. In GL(V), set g_1=diag(A,I), g_2=diag(I,A), and let s interchange the two summands. Then H=<g_1,g_2,s> is (C_3×C_3)⋊C_2 of order 18 and is solvable. The two C_3 factors afford nonisomorphic irreducible two-dimensional modules on the two summands; an H-invariant subspace is invariant under their normal product and is therefore a sum of selected summands, while s interchanges the summands. Thus only 0 and V are invariant. Hence G=V⋊H is a solvable primitive affine group of degree 16.

If this action were one-dimensional semilinear, H would embed in ΓL(1,16), whose order is (16-1)·4=60. Lagrange’s theorem forbids an order-18 subgroup because 18 does not divide 60. Therefore degree 16 is a counterexample, distinct from 9 and 25. Exact enumeration in `qa/MATHEMATICAL_CHECKS.json` verifies |H|=18 and irreducibility.

**Replacement theorem.** A finite solvable primitive permutation group is affine: it has a regular elementary-abelian minimal normal subgroup V and is V⋊H with H acting faithfully and irreducibly. Embedding H in ΓL(1,p^d) is an additional condition, not a consequence of solvability and primitivity.
