# POST-P13-A010 — W09-SE001 and Lemma III

Critical-layer certificate. The frozen 78-page P13R diplomatic edition is immutable.

**Status:** repaired

**Theorem (Bézout repair).** Let K be the coefficient field and V the separating resolvent. Suppose P(X) and Q(X,V) in K(V)[X] have exactly one common root a_i in a splitting field and all relevant roots are separable. Then a_i belongs to K(V).

**Proof.** The monic greatest common divisor D(X)=gcd(P,Q) has precisely the common roots, hence D(X)=X-a_i. The Euclidean algorithm in the PID K(V)[X] gives U(X)P(X)+W(X)Q(X,V)=X-a_i. Comparing constant terms, or evaluating the identity in the quotient algebra, expresses a_i as an element of K(V). Thus each root singled out by the resolvent is rational in V.

**Propagation.** Proposition I’s recovery of the roots from V is now proved. Every later substitution or resolvent construction that treats the roots as rational functions of V inherits this theorem. Tannery’s 1908 collation reports Galois’s own judgment that the abbreviated proof was insufficient.
