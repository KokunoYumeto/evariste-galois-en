# Galois 1897 GPT Critical Edition

**Post-P13 adjudication of the 21 deferred tasks**

Build date: 2026-08-13. This critical layer follows, and never rewrites, the frozen 78-page P13R diplomatic edition.

## Layer contract

The 1897 French diplomatic transcription is immutable evidence. Every emendation, theorem repair, counterexample, qualification, witness collation, and provenance conclusion appears only in this appendix and is keyed to the stable IDs already present in the P13R handoff. The words **repaired** and **rejected** refer to the critical adjudication of a printed claim; they never describe a mutation of the diplomatic source.

Active repaired candidate SHA-256: `4909FB4852F2178C583CCD425451E8BD5C7B02BD2346807F79F617BB3F2E645F`. P13R cold audit: PASS 74/74.

## Master disposition of the 21 tasks

| Task | Status | Result |
| --- | --- | --- |
| POST-P13-A001 | repaired | All 36 proved source-error records were adjudicated in a separate critical layer. Each has a proved repair, a qualified replacement, or a counterexample rejecting the printed claim; no diplomatic byte was changed. |
| POST-P13-A002 | proved | A machine-readable graph records local and cross-work dependencies. All downstream outcomes are classified as survives, survives under added hypotheses, or blocked. |
| POST-P13-A003 | proved | The dated prior-notice matrix covers all 36 errors and 15 variants. It distinguishes explicit notice, correct earlier witness, silent correction, candidate inaccessible errata source, and no notice found. |
| POST-P13-A004 | proved | The μ>ν argument survives: F_{p^ν}⊆F_{p^μ} gives ν\|μ, while the reciprocal rational dependence gives μ\|ν; hence μ=ν. The printed proof is compressed, not false. |
| POST-P13-A005 | rejected | The degree-9/25-only converse classification is false. A solvable primitive affine group of degree 16 and order 288 with irreducible complement of order 18 is not one-dimensional semilinear. |
| POST-P13-A006 | repaired | The p=11 row is reconstructed with 4 in place of the duplicated 5. The six-pair matching has stabilizer order 60 and index 11 in PSL(2,11). |
| POST-P13-A007 | proved | The 1846 witness prints réduction, the 1897 witness prints équation, and Tannery explicitly collates the substitution in 1908. The change affects semantic scope, not a formula. |
| POST-P13-A008 | unresolved_after_bounded_search | The 1897/1846 formula is exactly the standard Legendre relation under K/F notation. Tannery’s manuscript double-prime formula is not interpretable with enough certainty from the local notation; it has no downstream use in this volume. |
| POST-P13-A009 | proved | The 1846 witness has cette fonction at W09-PE001. W09-PE002 is diagnosed from the 1897 form proprieté itself; no 1846 comparison reading for that exact token was established. No explicit itemized notice was located for either record. |
| POST-P13-A010 | repaired | Lemma III is repaired by a gcd/Bézout argument in K(V)[X]. This closes Proposition I and later rational-resolvent uses. |
| POST-P13-A011 | repaired | Proposition II is replaced by the field-intersection/index theorem, and Proposition III by the normal-intersection proof. Composite-degree overstatement is rejected by an exact degree-4 example. |
| POST-P13-A012 | repaired | The fixed Fourier coefficient may vanish; the repair chooses a nonzero nontrivial coefficient guaranteed by Fourier inversion. The radical-tower step then survives. |
| POST-P13-A013 | repaired | The Kummer/normality hypotheses and the word nonidentity are restored. Proposition VIII survives; the unqualified Proposition VI statement is refuted by x^3-2. |
| POST-P13-A014 | proved | The W09 corpus was collated against 1846, Tannery 1908, the 1962/1976 critical-edition records, Neumann 2011/2013, and Dicker 2026. Prior art and no-notice findings are separated. |
| W10-DA001 | repaired | The printed unique-block proof is incomplete. A complete solvable-primitive proof uses a minimal normal elementary-abelian subgroup, whose orbits are blocks; it is transitive, regular, and yields affine degree p^d. |
| W10-DA002 | repaired | Affine linearity is valid under the inherited finite solvable primitive hypotheses. The unqualified primitive reading is false, for example for S_{p^2} in its natural primitive action. |
| W10-DA003 | rejected | The premise is rejected. Nineteenth-century conjugate/conjoined substitution terminology does not imply pairwise commutation; explicit conjugate projective maps on P¹(F7) fail to commute. |
| W10-DA004 | repaired | All six printed notation/formula repairs and both identity qualifications were propagated. The affine order counts survive; the terminal PDF089 p=3 inference remains blocked by W10-DA003. |
| W11-DA001 | proved | The earliest securely dated correction found is the Harvard-copy Wikisource page printing v, last modified 2018-07-22. Earlier item-level errata in the 1976 list could not be inspected. |
| W11-DA002 | unresolved_after_bounded_search | The local four digits remain fused. ETH provides an independent 1897 copy and IIIF/download metadata, but the high-resolution page bytes were not retrievable in the bounded environment; no character-by-character resolution is claimed. |
| W11-DA003 | proved | Replay proves the terminal topology: PDF091 predecessor blank, PDF092 historical contents, PDF093 colophon, and three distinct trailing blanks PDF094-096. |

## Critical errata catalogue: all 36 frozen IDs

### W02-PE001 — PDF 025 / L0024

**Adjudication:** `typographical_repair_proved`  
**Diplomatic printed form:** déveveloppent  
**Critical repair or replacement:** développent  
**Exact hypotheses:** none  
**Proof certificate:** French morphology and the immediate Picard-context establish that the duplicated syllable in déveveloppent is typographical. Picard’s 1897 Introduction has no 1846 parallel witness.  
**Propagation:** The Introduction’s meaning is unchanged.  
**Historical result:** No earlier witness exists for Picard’s 1897 Introduction. Modern comparison transcriptions normalize the form, but no explicit itemized erratum was found in the searched corpus.  
**Sources:** `SRC-LOCAL-1897;SRC-WIKI-1897`. The diplomatic layer is unchanged.

### W03-PE001 — PDF 035 / L0034

**Adjudication:** `formula_repair_proved`  
**Diplomatic printed form:** a + 1/(-1/B) = a - B; a - B  
**Critical repair or replacement:** Replace the printed letter a by p in the conjugate expression, giving p-B.  
**Exact hypotheses:** the article’s established integer-part symbol p  
**Proof certificate:** From x=p+1/A and the conjugate A↦-1/B, direct substitution gives p+1/(-1/B)=p-B.  
**Propagation:** The corrected conjugate and the following interval argument become coherent; no later work cites the misprinted letter.  
**Historical result:** No prior explicit notice found in the searched corpus.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W03-PE002 — PDF 035 / L0034

**Adjudication:** `sign_repair_proved`  
**Diplomatic printed form:** compris entre 0 et 1  
**Critical repair or replacement:** Replace “between 0 and 1” by the inequality -1<p-B<0.  
**Exact hypotheses:** B has integer part p and fractional part r in (0,1)  
**Proof certificate:** Write B=p+r with 0<r<1. Then p-B=-r, hence -1<-r<0.  
**Propagation:** Repairs the sign used in the conjugate-root discussion; no cross-work dependency.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W03-PE003 — PDF 037 / L0036

**Adjudication:** `formula_repair_proved`  
**Diplomatic printed form:** x = 3 - 1/A (printed as the full staircase reciprocal of the positive y expansion)  
**Critical repair or replacement:** Replace the second value 3-1/A by 3-A.  
**Exact hypotheses:** A is the positive root of 3A^2-2A-3=0  
**Proof certificate:** For A=(1+sqrt(10))/3, exact reduction gives 3(3-A)^2-16(3-A)+18=0, whereas the printed value has nonzero residual.  
**Propagation:** The final periodic continued fraction evaluates to 3-A; the theorem survives.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W04-SE001 — PDF 038 / L0037

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** Soient Fx et fx deux fonctions quelconques données; on aura, quels que soient x et h, [quotient]  
**Critical repair or replacement:** Restrict the quotient to pairs (x,h) for which f(x+h)≠f(x).  
**Exact hypotheses:** f(x+h)≠f(x)  
**Proof certificate:** For constant f the denominator vanishes for every x,h, so the printed universal quotient is undefined.  
**Propagation:** Only the domain of the displayed quotient changes.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897;SRC-NUMDAM-1846`. The diplomatic layer is unchanged.

### W04-SE002 — PDF 038 / L0037

**Adjudication:** `printed_claim_rejected_counterexample`  
**Diplomatic printed form:** ce qui démontre, a priori, l'existence des fonctions dérivées  
**Critical repair or replacement:** Delete the asserted a-priori existence of derivative functions; replace it by an explicit differentiability or quotient-limit hypothesis.  
**Exact hypotheses:** existence of the relevant two-sided limit, or differentiability assumptions  
**Proof certificate:** F(t)=|t|, f(t)=t at x=0 yields |h|/h with one-sided limits 1 and -1.  
**Propagation:** The following mean-value discussion can proceed only after the new hypothesis.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W04-SE003 — PDF 038 / L0037

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** donc on doit avoir aussi P = phi(k)  
**Critical repair or replacement:** Require ψ to be injective on the relevant range, or select and state a single inverse branch φ.  
**Exact hypotheses:** injectivity or a specified inverse branch  
**Proof certificate:** ψ(0)=ψ(1)=0 makes φ(ψ(P))=P impossible simultaneously for P=0,1.  
**Propagation:** The inversion step survives under the stated restriction.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W04-SE004 — PDF 038 / L0037

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** à moins qu'elle ne reste constante entre ces limites [...] cette fonction aura, entre x et x+h, un ou plusieurs maxima et minima  
**Critical repair or replacement:** Assume continuity on the closed interval; conclude at least one interior extremum unless the function is constant. Claim both a maximum and a minimum only when values occur on both sides of the common endpoint value.  
**Exact hypotheses:** continuity plus the indicated sign condition for two extrema  
**Proof certificate:** Without continuity, equal endpoint values do not imply attainment: F(0)=F(1)=0 and F(t)=t for 0<t<1 has no maximum.  
**Propagation:** Supplies the extremum needed for the mean-value argument; the stronger two-extrema wording is qualified.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W05-SE001 — PDF 040-041 / L0039-L0040

**Adjudication:** `printed_classification_rejected_counterexample`  
**Diplomatic printed form:** A part les cas mentionnés ci-dessous [...] deux quelconques de ses racines étant connues, les autres s’en déduisent rationnellement.  
**Critical repair or replacement:** Replace the finite exception list by the modern affine theorem: a finite solvable primitive group has a regular elementary-abelian socle and an irreducible point stabilizer; one-dimensional semilinearity is an additional restriction.  
**Exact hypotheses:** finite solvable primitive permutation group  
**Proof certificate:** A degree-8 AΓL(1,8) example already refutes the printed list. Independently, V=F2^4 with H=(C3×C3)⋊C2 of order 18 gives a solvable primitive degree-16 group not contained in ΓL(1,16), since 18 does not divide 60.  
**Propagation:** The later degree-9/25-only claim at PDF051 is also rejected; see POST-P13-A005.  
**Historical result:** No prior explicit notice of this exact counterexample was found; modern affine-group theory supplies the replacement framework.  
**Sources:** `SRC-LOCAL-1897;SRC-AFFINE-PRIMITIVE;SRC-LI-2003`. The diplomatic layer is unchanged.

### W05-SE002 — PDF 041 / L0040

**Adjudication:** `printed_claim_rejected_source_internal_correction`  
**Diplomatic printed form:** Au contraire, pour des degrés supérieurs, les équations modulaires ne peuvent s’abaisser.  
**Critical repair or replacement:** Qualify the impossibility statement by recording the p=7 and p=11 exceptional lowerings.  
**Exact hypotheses:** none beyond the modular-equation setting  
**Proof certificate:** Liouville’s footnote in the 1846 and 1897 printings explicitly records these exceptions; exact subgroup indices 7 and 11 corroborate the mechanism.  
**Propagation:** Feeds directly into W08-PE001’s p=11 matching.  
**Historical result:** Earliest explicit notice is Liouville’s 1846 footnote, reprinted in 1897.  
**Sources:** `SRC-LOCAL-1846;SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W06-PE001 — PDF 042 / L0041

**Adjudication:** `coherent_formula_reconstruction_proved_nonunique`  
**Diplomatic printed form:** x = psi x = nth_root( X / (x^n/Y) )  
**Critical repair or replacement:** In the critical layer use the symmetric candidate ψ(x)=(Y/(X/x^n))^{1/n}; do not assert that this is the unique historical correction.  
**Exact hypotheses:** X,Y and x nonzero where the quotient is formed, with compatible fixed radical branches; further monotonicity is required for bracketing  
**Proof certificate:** Exact polynomial examples prove that the printed map is not equivalent to X=Y and can lie on the same side of x as the first map. The symmetric candidate is algebraically equivalent to X=Y wherever denominators and the selected radical branches are defined.  
**Propagation:** The algebraic fixed-point equivalence is restored by this critical reconstruction, but the bracketing assertion still requires branch and monotonicity hypotheses; no later work uses the formula.  
**Historical result:** No prior explicit notice or uniquely documented historical emendation was found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W06-SE001 — PDF 043 / L0042

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** nX-xXprime > 0, nY-xYprime > 0; take k=(nX-xXprime) at x=1  
**Critical repair or replacement:** For X=Σ c_jx^j with c_j≥0, require at least one c_j>0 for j<n; analogously for Y.  
**Exact hypotheses:** x>0, nonnegative coefficients, and a positive coefficient below degree n  
**Proof certificate:** nX-xX′=Σ_{j<n}(n-j)c_jx^j. On x>0 it is strictly positive exactly when a lower-degree coefficient is positive.  
**Propagation:** The parameter k is then nonzero and the rational iteration is defined.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W07-SE001 — PDF 046 / L0045

**Adjudication:** `printed_example_rejected`  
**Diplomatic printed form:** x^2+x+1=0 mod 2 is offered as an example showing the roots are not expressible by radicals because the ordinary quadratic formula reduces to 0/0.  
**Critical repair or replacement:** Remove the example as evidence against radical expressibility; retain only the observation that the characteristic-zero quadratic formula degenerates.  
**Exact hypotheses:** none  
**Proof certificate:** A root α of x²+x+1 over F2 satisfies α³=1 and is itself a nontrivial cube root of unity.  
**Propagation:** No later finite-field construction depends on the invalid example.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W07-SE002 — PDF 049 / L0048

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** a^{m(p-1)}=1 and a_1^{m(p-1)}=1 are used without a nonzero qualification.  
**Critical repair or replacement:** Add a≠0 and a_1≠0 modulo p before applying Fermat’s theorem.  
**Exact hypotheses:** nonzero coefficients  
**Proof certificate:** Fermat’s relation u^{p-1}=1 holds on F_p^×. Exact enumeration confirms failure precisely when one selected coefficient is zero.  
**Propagation:** The worked choice a=-1,a_1=1 satisfies the repair, so its primitive-element conclusion survives.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W07-SE003 — PDF 050 / L0049

**Adjudication:** `algorithm_repaired`  
**Diplomatic printed form:** The same derivative-gcd method as for ordinary equations is said always to remove repeated roots.  
**Critical repair or replacement:** Add the characteristic-p branch: if F′=0, take a p-th root of F and recurse; otherwise perform squarefree factorization with gcd(F,F′).  
**Exact hypotheses:** perfect coefficient field or explicit p-th-root availability for the extraction step  
**Proof certificate:** For F=x³-1 over F3, F′=0 and F/gcd(F,F′)=1 loses the root.  
**Propagation:** Repairs the repeated-root algorithm; later finite-field factor selection survives.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W07-SE004 — PDF 050 / L0049

**Adjudication:** `formula_repair_proved`  
**Diplomatic printed form:** Integral solutions are obtained from gcd(F,x^{p-1}-1).  
**Critical repair or replacement:** Use gcd(F,x^p-x) to include every residue, or test x=0 separately before using x^{p-1}-1.  
**Exact hypotheses:** none  
**Proof certificate:** F=x has the integral solution 0, but gcd(x,x^{p-1}-1)=1.  
**Propagation:** The residue-root extraction algorithm then covers zero and nonzero roots.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W07-SE005 — PDF 050 / L0049

**Adjudication:** `formula_repair_proved`  
**Diplomatic printed form:** Solutions of order nu are said to be given by gcd(F,x^{p^nu-1}-1).  
**Critical repair or replacement:** For exact degree ν, remove all proper-subfield factors; equivalently use the product of monic irreducibles whose degrees equal ν, obtainable by Möbius inversion from x^{p^d}-x.  
**Exact hypotheses:** finite fields and the standard subfield lattice  
**Proof certificate:** x^{p^ν-1}-1 contains every nonzero element of F_{p^d} for d|ν; for p=3,ν=2, the degree-one element 1 is already a root.  
**Propagation:** The general factor-selection method survives after exact-degree isolation.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W08-PE001 — PDF 058 / L0057

**Adjudication:** `witness_supported_formula_repair`  
**Diplomatic printed form:** infinity, 1, 3, 5, 5, 9  
**Critical repair or replacement:** Replace the second 5 by 4, giving upper row ∞,1,3,4,5,9.  
**Exact hypotheses:** the displayed projective action  
**Proof certificate:** The corrected pairs partition P¹(F11); exact enumeration gives |PSL(2,11)|=660 and matching stabilizer 60, hence index 11.  
**Propagation:** Restores the p=11 modular lowering; no later proof in the volume depends on the duplicate.  
**Historical result:** The 1846 publication already prints 4, but no explicit erratum was found; earliest attested correct witness is 1846.  
**Sources:** `SRC-LOCAL-1846;SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W08-PE002 — PDF 058 / L0057

**Adjudication:** `witness_supported_lexical_repair`  
**Diplomatic printed form:** En toute rigueur, cette équation n’est pas possible dans les cas plus élevés.  
**Critical repair or replacement:** Replace équation by réduction in the critical layer.  
**Exact hypotheses:** none  
**Proof certificate:** The 1846 publication has réduction; Tannery’s 1908 collation identifies the 1897 substitution. Semantically, réduction names the degree-lowering operation under discussion, whereas équation does not.  
**Propagation:** No mathematical formula changes; the scope of the impossibility sentence is restored.  
**Historical result:** Correct in 1846; explicitly noticed by Tannery in 1908.  
**Sources:** `SRC-LOCAL-1846;SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W09-PE001 — PDF 065 / L0064

**Adjudication:** `witness_supported_lexical_repair`  
**Diplomatic printed form:** en permutant dans celle fonction  
**Critical repair or replacement:** Replace celle fonction by cette fonction.  
**Exact hypotheses:** none  
**Proof certificate:** The demonstrative must agree with fonction and the 1846 witness prints cette.  
**Propagation:** No mathematical dependency.  
**Historical result:** Correct in 1846; no explicit later notice found.  
**Sources:** `SRC-LOCAL-1846;SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W09-PE002 — PDF 071 / L0070

**Adjudication:** `typographical_repair_proved`  
**Diplomatic printed form:** proprieté  
**Critical repair or replacement:** Restore the accent: propriété.  
**Exact hypotheses:** none  
**Proof certificate:** The 1897 form proprieté is a missing-diacritic typographical error under standard French orthography. The local collation did not establish an 1846 comparison reading for this exact token.  
**Propagation:** No mathematical dependency.  
**Historical result:** No explicit prior notice or securely established earlier corrected witness was found in the searched corpus.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W09-SE001 — PDF 065-066 / L0064-L0065

**Adjudication:** `proof_gap_repaired`  
**Diplomatic printed form:** The unique common root is said to be “sought”, and the root is therefore declared rational in V.  
**Critical repair or replacement:** In K(V)[X], prove gcd(P,Q)=X-a_i and use a Bézout identity to express a_i rationally in V.  
**Exact hypotheses:** separability/distinct roots and uniqueness of the selected common root  
**Proof certificate:** Uniqueness of the common root makes the monic gcd linear; Euclid gives U P+V Q=X-a_i, hence a_i lies in K(V).  
**Propagation:** Closes Lemma III, Proposition I, and every later construction that treats roots as rational functions of the resolvent V.  
**Historical result:** Galois’s own insufficiency note for Lemma III is reported explicitly by Tannery in 1908. No earlier published Bézout repair was identified in the searched corpus.  
**Sources:** `SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W09-SE002 — PDF 069-070 / L0068-L0069

**Adjudication:** `theorem_repaired`  
**Diplomatic printed form:** After adjoining a root of an irreducible auxiliary equation, the group is unchanged or divides into p equal groups, although the prime-degree phrase defining p was deleted.  
**Critical repair or replacement:** Let L/K be the original splitting field, M=K(r), E=L∩M, H=Gal(L/E). Then [G:H]=[E:K] divides [M:K]. Recover the 1-or-p dichotomy only when [M:K]=p is prime.  
**Exact hypotheses:** finite separable splitting field; prime degree only for the dichotomy  
**Proof certificate:** The Galois correspondence gives H and the compositum degree formula gives [E:K]|[M:K]. The degree-4 element √2+√3 yields an index-2 counterexample to a composite-degree dichotomy.  
**Propagation:** Supplies the correct subgroup decomposition used in Proposition III and the radical tower.  
**Historical result:** Tannery 1908 records the deleted prime-degree wording and incompleteness; Dicker 2026 is a modern dedicated reconstruction.  
**Sources:** `SRC-LOCAL-1908;SRC-DICKER-2026`. The diplomatic layer is unchanged.

### W09-SE003 — PDF 070-071 / L0069-L0070

**Adjudication:** `proof_gap_repaired`  
**Diplomatic printed form:** The revised theorem is printed without its proof (“On trouvera la démonstration”).  
**Critical repair or replacement:** If M/K is a splitting field, E=L∩M is Galois over K, so H=Gal(L/E) is normal in G. Therefore all conjugate subgroups coincide after adjoining all auxiliary roots.  
**Exact hypotheses:** both L/K and M/K finite Galois  
**Proof certificate:** Intersections of finite normal separable extensions are normal and separable.  
**Propagation:** Repairs Proposition III and every later use of a common normal subgroup.  
**Historical result:** Tannery 1908 records the revised statement, erased predecessor proof, and Liouville interpolation. No prior published normal-intersection proof for this exact passage was identified in the searched corpus.  
**Sources:** `SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W09-SE004 — PDF 073 / L0072

**Adjudication:** `proof_gap_repaired`  
**Diplomatic printed form:** The proof adjoins the p-th root of one specifically displayed Fourier combination raised to p.  
**Critical repair or replacement:** Define all Fourier coefficients R_m=Σ ζ^{mj}θ_j and choose a nonzero coefficient with m≠0; do not privilege R_1.  
**Exact hypotheses:** p invertible in the base field and a primitive p-th root of unity available  
**Proof certificate:** A cyclic example has R_1=0 and R_2=3t. Fourier inversion shows all nontrivial coefficients cannot vanish unless the orbit is constant.  
**Propagation:** The selected nonzero R_m has invariant p-th power and supports the same radical adjunction.  
**Historical result:** No prior explicit notice found in the searched corpus.  
**Sources:** `SRC-LOCAL-1897;SRC-NEUMANN-2013`. The diplomatic layer is unchanged.

### W09-SE005 — PDF 075 / L0074

**Adjudication:** `missing_hypothesis_repaired`  
**Diplomatic printed form:** An irreducible prime-degree equation is said not to become reducible unless its group reduces to one permutation.  
**Critical repair or replacement:** Require the radical extension to be cyclic Galois of prime degree in the inherited Kummer setting. Then reducibility of a prime-degree irreducible polynomial forces the relevant normal subgroup to be trivial, hence complete splitting.  
**Exact hypotheses:** base contains the needed roots of unity; radical extension irreducible, cyclic, Galois, and prime degree  
**Proof certificate:** x³-2 over Q becomes reducible over Q(∛2) but does not split. Under normal prime-degree Kummer hypotheses, subgroup orbits form a block system, so nontransitive normal subgroup is trivial.  
**Propagation:** Propositions VI-VII survive only within this Kummer context.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897;SRC-NEUMANN-2013`. The diplomatic layer is unchanged.

### W09-SE006 — PDF 078 / L0077

**Adjudication:** `missing_qualifier_repaired`  
**Diplomatic printed form:** The affine substitution x_k↦x_{ak+b} is said never to leave two letters in place, with no exclusion of the identity.  
**Critical repair or replacement:** Insert nonidentity before the affine fixed-point claim.  
**Exact hypotheses:** none  
**Proof certificate:** For k↦ak+b, the identity fixes all p points; a nonidentity map fixes zero points if a=1,b≠0 and exactly one if a≠1.  
**Propagation:** Proposition VIII’s two-root criterion survives because only nonidentity elements are relevant.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W10-PE001 — PDF 082 / L0081

**Adjudication:** `witness_supported_index_repair`  
**Diplomatic printed form:** a_{k_1,k_1,k_3,\ldots,k_\mu}  
**Critical repair or replacement:** Replace the repeated k_1 by k_2.  
**Exact hypotheses:** none  
**Proof certificate:** The declared independent indices require k_1,k_2,… and Tannery explicitly records the correction.  
**Propagation:** Restores the coordinate tuple; subsequent affine construction survives.  
**Historical result:** Explicitly corrected by Tannery in 1908.  
**Sources:** `SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W10-PE002 — PDF 082 / L0081

**Adjudication:** `witness_supported_index_repair`  
**Diplomatic printed form:** \psi(k)_2  
**Critical repair or replacement:** Read ψ(k_2), not ψ(k)_2.  
**Exact hypotheses:** none  
**Proof certificate:** Coordinate parallelism and Tannery’s correction agree.  
**Propagation:** Restores the second coordinate function.  
**Historical result:** Explicitly corrected by Tannery in 1908.  
**Sources:** `SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W10-PE003 — PDF 083 / L0082

**Adjudication:** `witness_supported_index_repair`  
**Diplomatic printed form:** a_{mk_1+n k_2}  
**Critical repair or replacement:** Read a_{mk_1+n,k_2}.  
**Exact hypotheses:** none  
**Proof certificate:** The transformation changes the first coordinate and leaves the second fixed; Tannery gives the separated pair.  
**Propagation:** The one-coordinate affine action and later two-coordinate action remain coherent.  
**Historical result:** Explicitly corrected by Tannery in 1908.  
**Sources:** `SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W10-PE004 — PDF 083 / L0082

**Adjudication:** `context_forced_index_repair`  
**Diplomatic printed form:** a_{k_2,k_3}  
**Critical repair or replacement:** Read a_{k_1,k_2}.  
**Exact hypotheses:** none  
**Proof certificate:** Only k_1,k_2 have been introduced in the section, and the target has those two coordinates.  
**Propagation:** Restores a map on the stated domain.  
**Historical result:** No explicit prior notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W10-PE005 — PDF 084 / L0083

**Adjudication:** `witness_supported_formula_repair`  
**Diplomatic printed form:** a_{m_1k_1+n_1k+\alpha_1m_2k_1+n_2k_2+\alpha_2}  
**Critical repair or replacement:** Reconstruct formula (A) as a_{m_1k_1+n_1k_2+α_1, m_2k_1+n_2k_2+α_2}.  
**Exact hypotheses:** invertible linear part where a permutation is intended  
**Proof certificate:** It is the affine form forced by the finite-difference condition and is explicitly supplied by Tannery.  
**Propagation:** The affine-linearity argument can then be stated correctly under W10-DA002’s inherited solvability hypotheses.  
**Historical result:** Explicitly corrected by Tannery in 1908.  
**Sources:** `SRC-LOCAL-1897;SRC-LOCAL-1908`. The diplomatic layer is unchanged.

### W10-PE006 — PDF 088 / L0087

**Adjudication:** `formula_repair_proved`  
**Diplomatic printed form:** (rk+s)k-m(mk+n)=0  
**Critical repair or replacement:** Remove the extra factor m: (rk+s)k-(mk+n)=0.  
**Exact hypotheses:** projective denominator treated in P¹  
**Proof certificate:** This is the direct fixed-point equation of T(k)=(mk+n)/(rk+s); its discriminant is the next printed expression (m-s)^2+4nr.  
**Propagation:** Restores the fixed-point/support trichotomy; the p=3 terminal argument still fails independently under W10-DA003.  
**Historical result:** The same error occurs in 1846; no explicit erratum was found.  
**Sources:** `SRC-LOCAL-1846;SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W10-SE001 — PDF 086 / L0085

**Adjudication:** `missing_qualifier_repaired`  
**Diplomatic printed form:** m est nécessairement <2 et ... 0 ou 1  
**Critical repair or replacement:** Insert nonidentity before asserting fixed-space dimension <2.  
**Exact hypotheses:** none  
**Proof certificate:** A nonidentity affine map has empty fixed set or an affine fixed set of dimension 0 or 1; the identity has dimension 2.  
**Propagation:** The divisibility bound survives; the identity is handled separately.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W10-SE002 — PDF 087 / L0086

**Adjudication:** `count_repaired`  
**Diplomatic printed form:** dans ces substitutions, aucune lettre ne reste à la même place, et elles sont au nombre de p^2-1  
**Critical repair or replacement:** Replace p²-1 by p²-2 in the count of nonidentity scalars moving every nonzero letter; retain subgroup order p²-1.  
**Exact hypotheses:** none  
**Proof certificate:** The scalar group contains identity; every other scalar fixes only zero.  
**Propagation:** The final affine-group order p²(p²-1)(p²-p) is unchanged.  
**Historical result:** No prior explicit notice found.  
**Sources:** `SRC-LOCAL-1897`. The diplomatic layer is unchanged.

### W11-PE001 — PDF 092 / L0091

**Adjudication:** `page_reference_repair_proved`  
**Diplomatic printed form:** 1  
**Critical repair or replacement:** Replace the table-of-contents page reference 1 by roman v in the critical layer.  
**Exact hypotheses:** none  
**Proof certificate:** The Introduction occupies logical folios v-x by the primary page map; the 1897 table prints Arabic 1.  
**Propagation:** Only the critical navigation reference changes.  
**Historical result:** A Harvard-copy Wikisource transcription silently prints v and was last modified 2018-07-22; this is the earliest securely dated notice found.  
**Sources:** `SRC-LOCAL-1897;SRC-WIKI-TOC;SRC-ETH-1897`. The diplomatic layer is unchanged.

## The 21 task certificates

## POST-P13-A001 — complete errata repair

**Status:** repaired

This certificate belongs to the critical layer. The P13R diplomatic transcription and its 78-page PDF are immutable. No wording below authorizes a silent change to that layer. Coordinates are physical PDF/JP2 coordinates from the frozen map.

**Theorem.** Every one of the 36 records in `CRITICAL_ERRATA_CATALOGUE.csv` has been closed by exactly one of the following critical actions: a typographical or formula repair proved from the 1897 context and another witness; an added hypothesis proved necessary and sufficient for the local step; a replacement proof; or a counterexample rejecting the printed universal claim.

**Proof.** The catalogue is an exact join with the frozen 36-row source-error ledger. Its `error_id` set is identical, every row states `diplomatic_layer_mutated=no`, and each row has a nonempty adjudication, repair, proof, propagation outcome, and prior-notice outcome. Exact symbolic and finite-group checks are in `qa/MATHEMATICAL_CHECKS.json`. No record has been deleted, merged, or renumbered.

The principal nonlocal replacements are: the affine primitive theorem for W05-SE001 and POST-P13-A005; the characteristic-p squarefree and exact-degree algorithms for W07-SE003–005; the field-intersection, Bézout, Fourier, and Kummer repairs for W09-SE001–006; and the minimal-normal-subgroup affine proof for W10-DA001–002. The remaining entries are local textual, sign, formula, index, or identity corrections.

**Conclusion.** The errata layer is complete as an adjudication of the frozen 36 records. It is not a translation and it does not assert that every diagnosis is historically new.

## POST-P13-A002 — dependency and propagation

**Status:** proved

This certificate belongs to the critical layer. The P13R diplomatic transcription and its 78-page PDF are immutable. No wording below authorizes a silent change to that layer. Coordinates are physical PDF/JP2 coordinates from the frozen map.

**Theorem.** `DEPENDENCY_PROPAGATION_EDGES.csv` records every material downstream dependency of the 36 repairs and the four deferred proof audits.

**Proof.** Local typographical errors terminate inside their work. W05-SE002 points to W08-PE001; W05-SE001 points to the PDF051 classification. W09-SE001 feeds Proposition I and rational resolvents; W09-SE002 and W09-SE003 feed the normal-subgroup decomposition; W09-SE004 feeds the radical resolvent; W09-SE005–006 feed Propositions VII–VIII. The W10 index repairs feed the affine coordinate maps, while PE006 feeds the support trichotomy and DA003 independently blocks the terminal p=3 inference. Each edge is labelled by type and by one of the outcomes “survives,” “survives under hypotheses,” or “blocked.”

No later page silently inherits an unrepaired false statement. The diplomatic text remains historical evidence; the graph belongs to the critical layer.

## POST-P13-A003 — historical and modern prior-notice search

**Status:** proved

This certificate belongs to the critical layer. The P13R diplomatic transcription and its 78-page PDF are immutable. No wording below authorizes a silent change to that layer. Coordinates are physical PDF/JP2 coordinates from the frozen map.

**Method.** The bounded corpus comprised the local 1846, 1897, and 1908 witnesses; Numdam and EuDML records; the independent ETH 1897 copy metadata; the Harvard-copy Wikisource transcription and revision record; the 1962 and 1976 Bourgne–Azra critical-edition records; Neumann’s 2011/2013 edition record; Dicker’s 2026 Proposition-II paper; and exact-phrase web searches logged in `SEARCH_QUERY_LEDGER.csv`.

**Result.** The 51-row `BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv` distinguishes (i) explicit notice, (ii) a correct earlier witness without explicit erratum, (iii) a dated silent correction, (iv) an inaccessible candidate errata source, and (v) no prior notice found in the searched corpus. The 1976 printing is known from René Taton’s 1977 review to contain an errata list and two concordances, but its item-level errata were not accessible; it is therefore never used as proof that a particular error was previously noticed.

**Conclusion.** No record is called new. Negative results are bounded search results only.

## POST-P13-A004 — PDF047 finite-field degree argument

**Status:** proved

**Theorem.** Under the dependencies printed in the argument, the allegedly larger degree μ cannot exceed ν; in fact μ=ν.

**Proof.** Let the initial root i generate the finite field F_{p^μ}. The construction writes the coefficients and hence the selected quantities in the field generated by i, so the field F_{p^ν} generated by the constructed element is a subfield of F_{p^μ}. The finite-field subfield theorem gives ν|μ. Conversely, the text states that i is a rational function of the constructed quantity; therefore F_{p^μ} is a subfield of F_{p^ν}, giving μ|ν. Hence μ=ν. The compressed source does not spell out both inclusions or invoke the subfield theorem, but its conclusion is correct.

**Disposition.** No new source-error ID is created. The critical layer supplies the omitted inclusions and divisibilities.

## POST-P13-A005 — PDF051 converse and the degree-9/25 exceptions

**Status:** rejected

**Theorem.** The printed claim that the only exceptional solvable primitive degrees outside the one-dimensional semilinear form are 9 and 25 is false.

**Counterexample.** Let W=F_2^2 and V=W⊕W. Let A=[[0,1],[1,1]] of order 3. In GL(V), set g_1=diag(A,I), g_2=diag(I,A), and let s interchange the two summands. Then H=<g_1,g_2,s> is (C_3×C_3)⋊C_2 of order 18 and is solvable. The two C_3 factors afford nonisomorphic irreducible two-dimensional modules on the two summands; an H-invariant subspace is invariant under their normal product and is therefore a sum of selected summands, while s interchanges the summands. Thus only 0 and V are invariant. Hence G=V⋊H is a solvable primitive affine group of degree 16.

If this action were one-dimensional semilinear, H would embed in ΓL(1,16), whose order is (16-1)·4=60. Lagrange’s theorem forbids an order-18 subgroup because 18 does not divide 60. Therefore degree 16 is a counterexample, distinct from 9 and 25. Exact enumeration in `qa/MATHEMATICAL_CHECKS.json` verifies |H|=18 and irreducibility.

**Replacement theorem.** A finite solvable primitive permutation group is affine: it has a regular elementary-abelian minimal normal subgroup V and is V⋊H with H acting faithfully and irreducibly. Embedding H in ΓL(1,p^d) is an additional condition, not a consequence of solvability and primitivity.

## POST-P13-A006 — W08-PE001 and the p=11 lowering

**Status:** repaired

**Theorem.** Replacing the repeated 5 by 4 yields the corrected matching

{∞,0}, {1,2}, {3,6}, {4,8}, {5,10}, {9,7}

on P^1(F_11). Its setwise stabilizer in PSL(2,11) has order 60 and index 11.

**Proof.** The twelve entries are now all distinct, so the six pairs partition the projective line. Exact enumeration of determinant-one fractional-linear transformations modulo scalar sign gives |PSL(2,11)|=660. Testing the induced action on the six unordered pairs gives 60 stabilizing elements. The index is 660/60=11, supplying the degree-11 resolvent/lowering structure. The 1846 publication prints 4; the 1897 edition alone duplicates 5.

**Propagation.** The correction restores the example promised by Liouville’s p=11 exception. It does not alter the diplomatic letter.

## POST-P13-A007 — W08-PE002, équation/réduction

**Status:** proved

**Collation.** The 1846 publication reads “cette réduction n’est pas possible.” The 1897 edition reads “cette équation n’est pas possible.” Tannery’s 1908 collation explicitly reports the manuscript/Liouville reading and the later substitution.

**Semantic certificate.** The antecedent is the lowering of a modular equation from degree p+1 to degree p. “Réduction” names that operation. “Équation” instead makes the sentence say that the equation itself is impossible, which is not the mathematical assertion being discussed. The critical reading is therefore “réduction.”

**Downstream effect.** No displayed formula changes. The correction narrows the impossibility claim to the degree-lowering operation and aligns it with the p=7 and p=11 exceptions.

## POST-P13-A008 — W08-WV001, Legendre relation

**Status:** unresolved_after_bounded_search

**Proved part.** The 1897 and 1846 formula FE′+EF′−FF′=π/2 is the standard Legendre relation when F denotes the complete elliptic integral K and the prime denotes complementary modulus: EK′+E′K−KK′=π/2. This agrees exactly with DLMF 19.7.1.

**Unresolved part.** Tannery reports a manuscript formula F′F″−E″F′=(π/2)√−1. The local collation does not define the single- and double-prime conventions sufficiently to determine whether this is a transformed Legendre relation, a different period relation, or a manuscript error. No downstream argument in the 1897 letter uses either formula, so the ambiguity has no propagated mathematical effect.

**Bounded-search conclusion.** Historical and modern searches found the standard printed relation, but no secure adjudication of the manuscript double-prime formula. The variant remains unresolved; neither witness is fused into the other.

## POST-P13-A009 — W09-PE001 and W09-PE002

**Status:** proved

**Collation.** At PDF065 the 1897 edition prints “celle fonction,” whereas the 1846 publication prints “cette fonction.” At PDF071 the 1897 edition prints “proprieté.” The local 1846 collation did not establish a comparison reading for that exact token, and no manuscript-collation source supplies a competing substantive reading.

**Conclusion.** Both are textual errors: the former is a demonstrative-agreement error supported by a correct 1846 witness; the latter is a missing diacritic established from the 1897 spelling and French orthography. The critical layer restores “cette fonction” and “propriété,” but records distinct provenance classes. Exact-phrase and edition searches found no explicit itemized notice; the matrix makes no novelty claim.

## POST-P13-A010 — W09-SE001 and Lemma III

**Status:** repaired

**Theorem (Bézout repair).** Let K be the coefficient field and V the separating resolvent. Suppose P(X) and Q(X,V) in K(V)[X] have exactly one common root a_i in a splitting field and all relevant roots are separable. Then a_i belongs to K(V).

**Proof.** The monic greatest common divisor D(X)=gcd(P,Q) has precisely the common roots, hence D(X)=X-a_i. The Euclidean algorithm in the PID K(V)[X] gives U(X)P(X)+W(X)Q(X,V)=X-a_i. Comparing constant terms, or evaluating the identity in the quotient algebra, expresses a_i as an element of K(V). Thus each root singled out by the resolvent is rational in V.

**Propagation.** Proposition I’s recovery of the roots from V is now proved. Every later substitution or resolvent construction that treats the roots as rational functions of V inherits this theorem. Tannery’s 1908 collation reports Galois’s own judgment that the abbreviated proof was insufficient.

## POST-P13-A011 — W09-SE002 and W09-SE003

**Status:** repaired

**Theorem (intersection/index).** Let $L/K$ be the original splitting field, $M=K(r)$ an auxiliary extension, $E=L\cap M$, $G=\operatorname{Gal}(L/K)$, and $H=\operatorname{Gal}(L/E)$. Then $[G:H]=[E:K]$ and $[E:K]\mid[M:K]$.

**Proof.** The Galois correspondence gives $[G:H]=[E:K]$. Since $E$ is a subfield of $M$, the tower law gives $[M:K]=[M:E][E:K]$. If $[M:K]=p$ is prime, the index is $1$ or $p$. Without prime degree the dichotomy is false: $r=\sqrt2+\sqrt3$ has degree $4$, contains $\mathbf Q(\sqrt2)$, and reduces its $C_2$ splitting group with index $2$.

**Theorem (Proposition III normality).** If $M/K$ is also a splitting field, then $E/K$ is finite Galois, so $H$ is normal in $G$. Consequently the subgroups arising from conjugate auxiliary roots coincide after all auxiliary roots are adjoined.

**Propagation.** These two theorems replace the undefined p and the omitted proof. They control all dependent group decompositions and the subsequent radical tower.

## POST-P13-A012 — W09-SE004 Fourier coefficient

**Status:** repaired

**Theorem.** Let θ_0,…,θ_{p-1} be a nonconstant cyclic orbit and ζ a primitive p-th root of unity. At least one nontrivial Fourier coefficient R_m=Σ_j ζ^{mj}θ_j, 1≤m≤p-1, is nonzero.

**Proof.** Fourier inversion gives θ_j=p^{-1}Σ_m ζ^{-mj}R_m. If every R_m for m≠0 vanished, every θ_j would equal p^{-1}R_0, contradicting nonconstancy. The printed choice R_1 need not work: for p=3 and θ_j=1+ω^j t, one has R_1=0 but R_2=3t≠0.

A cyclic shift multiplies R_m by a p-th root of unity, so R_m^p is invariant. Choosing a nonzero nontrivial coefficient therefore supplies the intended radical adjunction. The radical-tower conclusion survives with this selection rule.

## POST-P13-A013 — W09-SE005, W09-SE006, Propositions VII-VIII

**Status:** repaired

**Counterexample to the unqualified reducibility claim.** The irreducible polynomial X^3-2 becomes reducible over Q(∛2) but does not split; the residual quadratic has negative discriminant in the real embedding. Thus reducibility does not force the group to become trivial in an arbitrary radical extension.

**Kummer repair.** Let K contain the relevant p-th roots of unity and let M/K be an irreducible cyclic Galois Kummer extension of prime degree p. For an irreducible polynomial of prime degree n with splitting field L, put H=Gal(L/L∩M). Then H is normal. Its orbits form a block system in a prime-degree transitive action, so H is transitive or trivial. If the polynomial becomes reducible over M, H is not transitive and is therefore trivial; the polynomial splits completely. This is the context in which Propositions VI-VII survive.

**Affine repair.** In Proposition VIII insert “nonidentity.” The identity k↦k fixes every letter; a nonidentity affine map k↦ak+b fixes at most one. Hence adjoining two roots kills every nonidentity group element, and the final affine necessity/sufficiency argument survives.

## POST-P13-A014 — W09 provenance corpus

**Status:** proved

This certificate belongs to the critical layer. The P13R diplomatic transcription and its 78-page PDF are immutable. No wording below authorizes a silent change to that layer. Coordinates are physical PDF/JP2 coordinates from the frozen map.

The six W09 witness variants are all explicitly grounded in Tannery’s 1908 collation: omitted definitions, Lemma III’s insufficiency, deletion of the prime-degree phrase, the revised Proposition III, a marginal construction sentence, and the expanded Cauchy citation. The 1846 witness supplies the correct form for W09-PE001; W09-PE002 is diagnosed from the 1897 spelling itself, without a securely established 1846 comparison token. The 1962 critical edition is bibliographically verified; a 1977 review verifies that the 1976 facsimile printing added supplementary pages containing an errata list and two concordances, but the item-level entries were inaccessible. Neumann’s 2011 book has a corrected second printing dated September 2013. Dicker’s paper submitted July 22, 2026 specifically reconstructs Proposition II, not Lemma III or Proposition III.

The matrix records these as established prior art where direct evidence exists. W09-SE004–006 are recorded as “no prior notice found in the searched corpus,” not as new results.

## W10-DA001 — prime-power theorem and unique blocks

**Status:** repaired

**Theorem.** A finite solvable primitive permutation group G has degree p^d and embeds in AGL(d,p).

**Proof.** Choose a minimal nontrivial normal subgroup N of G. Solvability makes N elementary abelian of order p^d. The N-orbits form a G-invariant block system; primitivity makes N transitive. Since N is abelian, a point stabilizer N_α is normal in G: all point stabilizers in N are equal by abelianness and their intersection is the kernel of the faithful action, hence trivial. Thus N is regular. Identifying the points with N gives an affine space over F_p. A point stabilizer H acts faithfully by conjugation on N and is irreducible, because an H-invariant proper nonzero subgroup of N would yield a nontrivial block system. Hence G=N⋊H≤AGL(d,p).

**Disposition.** The printed unique-block construction is incomplete but its prime-power conclusion survives under the inherited finite solvable primitive hypotheses.

## W10-DA002 — affine linearity

**Status:** repaired

**Qualified theorem.** Under the inherited hypotheses that the permutation group is finite, solvable, and primitive of degree p^d, W10-DA001 identifies the letters with the regular elementary-abelian socle V and identifies the point stabilizer with an irreducible subgroup of GL(V). Every group element is therefore affine: x↦Ax+b.

**Failure of the unqualified reading.** Primitivity alone does not imply affine linearity. For example, S_{p^2} in its natural action is primitive, but for p^2≥5 it has nonabelian simple socle A_{p^2} and no regular elementary-abelian normal subgroup. It cannot be an affine group of degree p^2.

**Conclusion.** Formula (A), after W10-PE005 is repaired, is valid only inside the inherited solvable-primitive argument.

## W10-DA003 — PDF089 conjuguées and pairwise equality

**Status:** rejected

**Historical finding.** Cauchy’s technical phrase “système de substitutions conjuguées” designated what modern historians translate as a “system of conjoined substitutions,” namely a substitution system closed under composition; Hollings explicitly warns that the translation “conjugate substitutions” is best avoided because of its modern group-theoretic meaning. In the PDF089 sentence, the immediately preceding clause already says that the substitutions are transformed into one another by the translations \((k,k+m)\). Thus the historically supportable force is membership in, or transport within, the relevant closed substitution system/orbit—not pairwise commutativity. The lexical evidence does not establish a stronger relation.

**Exact counterexample in the printed projective family.** On P^1(F_7), set T_m(k)=m+1/(k-m), with the usual values at infinity. Translation τ_1 conjugates T_0 to T_1. Nevertheless direct evaluation shows T_0T_1≠T_1T_0. Thus even two members related by the evident translation conjugacy fail to commute.

**Consequence.** Neither the historically attested “conjoined-system” sense nor modern element conjugacy implies pairwise commutativity. The premise used at PDF089 is therefore unsupported; under modern conjugacy it is explicitly false. The terminal p=3 conclusion depending on it is blocked. No diplomatic wording is changed.

## W10-DA004 — propagation through the p-power and p^2 arguments

**Status:** repaired

W10-PE001–PE004 restore the coordinate tuples and maps on PDF082–083. W10-PE005 restores the two-dimensional affine formula; with W10-DA001–002 it expresses the solvable primitive group as an affine group. W10-SE001 adds the nonidentity qualification to the fixed-space dimension count; its divisibility conclusion survives. W10-SE002 changes only the count of fixed-point-free nonidentity scalars from p^2-1 to p^2-2; the scalar subgroup order p^2-1 and total affine group order p^2(p^2-1)(p^2-p) survive. W10-PE006 restores the projective fixed-point equation and makes the printed discriminant correct, so the support-size trichotomy survives.

The final PDF089 pairwise-commutativity premise does not survive, by W10-DA003. Accordingly, the p=3 terminal inference is not carried into the corrected theorem set.

## W11-DA001 — table-of-contents 1 to v

**Status:** proved

The frozen page map and the primary 1897 images place Picard’s Introduction on roman folios v-x. The 1897 table of contents nevertheless prints Arabic 1. An independent Harvard-copy Wikisource transcription prints v; its permanent page record states that the page was last modified on July 22, 2018. This is the earliest securely dated correction located in the accessible corpus.

The ETH catalogue proves the existence of an independent 1897 copy (Rar 4575, DOI 10.3931/e-rara-19915), but item-level comparison was not retrievable. The 1976 Bourgne–Azra printing is known to add an errata list, but that list was not accessible, so no earlier item-level notice is claimed.

## W11-DA002 — printer job number

**Status:** unresolved_after_bounded_search

The four small digit bodies at PDF093 remain fused in the bitonal primary image. The existing raw and conservatively enhanced crops do not support a character-by-character reading. An independent ETH 1897 copy was located, with DOI, IIIF manifest link, and downloadable PDF metadata, but the high-resolution page bytes could not be fetched in the bounded environment. The Harvard Wikisource colophon transcription omits the job number, and no printer record was located.

The unresolved reading W11-U001 is therefore retained unchanged. Resolution requires either a retrievable high-resolution independent copy of the colophon leaf or Gauthier-Villars printer records that identify the job number. No digits are guessed.

## W11-DA003 — terminal topology and P10/P11 boundary

**Status:** proved

Replay of the primary PDF, JP2 leaves, disposition map, and integrated candidate gives the following exact topology: PDF091/L0090 is the predecessor blank owned by W10; PDF092/L0091 is the historical table of contents; PDF093/L0092 is the colophon; PDF094/L0093, PDF095/L0094, and PDF096/L0095 are three distinct trailing blanks. The P10/P11 boundary introduces no text join. The corrected critical page reference v does not alter the historical table in the diplomatic layer.

All six physical leaves remain dispositioned exactly once. The one-click reader preserves the frozen 78-page diplomatic PDF as its prefix; the critical appendix follows it and does not collapse any blank topology.

## Unresolved readings and variants after bounded completion

Five records remain open in the complete cumulative handoff. Two were active post-P13 questions that remain unresolved after bounded search: the manuscript notation in W08-WV001 and the four-digit job number W11-U001. The three W01 image readings remain unresolved exactly as frozen and are carried forward outside the mathematical post-P13 scope. Nothing has been guessed or silently dropped.

| record_id | status | missing_evidence |
| --- | --- | --- |
| W01-U001 | carried forward unresolved outside 21 task scope | A character-resolved independent image or documented portrait-plate source sufficient to read the faint lower-left signature on PDF019. |
| W01-U002 | carried forward unresolved outside 21 task scope | Independent provenance evidence sufficient to adjudicate the relation between the degraded PDF021 portrait and PDF019 without silently deduplicating witnesses. |
| W01-U003 | carried forward unresolved outside 21 task scope | A higher-fidelity device image or printer-source record sufficient to expand the publisher-device ribbon legend character by character. |
| W08-WV001 | unresolved after bounded search | A notation-keyed manuscript or scholarly adjudication sufficient to interpret F-prime/F-double-prime/E-double-prime and test equivalence. |
| W11-U001 | unresolved after bounded search | Character-resolved independent colophon image or Gauthier-Villars printer register. |

## Historical-priority conclusions

Direct evidence establishes Liouville’s 1846 footnote as notice of the p=7 and p=11 modular exceptions; Tannery’s 1908 collation as explicit notice of multiple W08-W10 editorial and proof defects; the 1976 Bourgne-Azra printing as containing an added errata list whose item-level contents were unavailable; and the Harvard-copy Wikisource page as a dated silent correction of the contents reference to roman v on July 22, 2018. All other negative findings are stated only as “no prior notice found in the searched corpus.”

## Bibliographic sources

- **SRC-LOCAL-1897.** Évariste Galois; Société mathématique de France; introduction by Émile Picard, *Œuvres mathématiques d'Évariste Galois* (1897), Paris: Gauthier-Villars et Fils, physical PDF 1-96; printed x, 1-61 plus back matter.
- **SRC-LOCAL-1846.** Évariste Galois; edited by Joseph Liouville, *Œuvres mathématiques* (1846), Journal de Mathématiques Pures et Appliquées, série 1, vol. 11, 381-444; local PDF 1-65. <https://www.numdam.org/item/JMPA_1846_1_11__381_0/>
- **SRC-LOCAL-1908.** Jules Tannery, editor, *Manuscrits d'Évariste Galois* (1908), Paris: Gauthier-Villars, local PDF 1-77; Commons scan 87 leaves. <https://commons.wikimedia.org/wiki/File:Galois_-_Manuscrits,_édition_Tannery,_1908.djvu>
- **SRC-NUMDAM-1846.** Numdam, *Numdam record for the 1846 publication* (1846/online), Numdam item: JMPA 1846, series 1, volume 11, page 381, 381-444; record marks corrected-by Errata. <https://www.numdam.org/item/JMPA_1846_1_11__381_0/>
- **SRC-ETH-1897.** ETH-Bibliothek Zürich, *ETH-Bibliothek independent copy of Oeuvres mathématiques* (1897; online 2013-10-08), Rar 4575; DOI 10.3931/e-rara-19915, X, 61 pages, one leaf. <https://www.e-rara.ch/zut/content/titleinfo/6262819>
- **SRC-WIKI-1897.** French Wikisource contributors, *Harvard College Library 1897 copy transcription* (1897 scan; current online transcription), Gauthier-Villars 1897, complete index. <https://fr.wikisource.org/wiki/Livre:Galois_-_Œuvres_mathématiques,_Gauthier-Villars,_1897.djvu>
- **SRC-WIKI-TOC.** French Wikisource contributors, *1897 table-of-contents transcription, page 91* (last modified 2018-07-22), oldid 7722271, page 91. <https://fr.wikisource.org/w/index.php?title=Page:Galois_-_Œuvres_mathématiques,_Gauthier-Villars,_1897.djvu/91&oldid=7722271>
- **SRC-DLMF-LEGENDRE.** NIST Digital Library of Mathematical Functions, *DLMF §19.7(i), Legendre's Relation* (current reference), Equation 19.7.1, §19.7(i). <https://dlmf.nist.gov/19.7.E1>
- **SRC-BOURGNE-AZRA-1962.** Robert Bourgne and Jean-Pierre Azra, editors, *Écrits et mémoires mathématiques d'Évariste Galois* (1962), Gauthier-Villars; xxii+541 pp., critical edition. <https://doi.org/10.1017/S0008439500026989>
- **SRC-BOURGNE-AZRA-1976.** Robert Bourgne and Jean-Pierre Azra, editors, *Écrits et mémoires mathématiques d'Évariste Galois, 2e éd.* (1976), new facsimile printing with supplementary errata and two concordances, xxxi+541 pp.. <https://www.persee.fr/doc/rhs_0151-4105_1977_num_30_2_1486>
- **SRC-NEUMANN-2013.** Peter M. Neumann, *The mathematical writings of Évariste Galois* (2011; corrected second printing September 2013), EMS Heritage of European Mathematics 104, 1-410. <https://ems.press/books/hem/102/contents>
- **SRC-DICKER-2026.** Math Dicker, *The Significance of Proposition II in Galois' Mémoire, The Origin of Galois Automorphisms* (2026-07-22), arXiv:2607.20147, abstract and paper. <https://arxiv.org/abs/2607.20147>
- **SRC-CAUCHY-TERMS.** Christopher D. Hollings, *‘Nobody could possibly misunderstand what a group is’: a study in early twentieth-century group axiomatics* (2017), Archive for History of Exact Sciences 71, 409–481, especially §2.1 on early substitution terminology. <https://doi.org/10.1007/s00407-017-0193-8>
- **SRC-AFFINE-PRIMITIVE.** Attila Maróti and Saveliy V. Skresanov, *Bounds for the Diameters of Orbital Graphs of Affine Groups* (2023), Vietnam Journal of Mathematics 51, 617–631; introductory definition of affine primitive groups. <https://doi.org/10.1007/s10013-023-00607-5>
- **SRC-LI-2003.** Cai Heng Li, *The Finite Primitive Permutation Groups Containing an Abelian Regular Subgroup* (2003), Proc. London Math. Soc. 87, 725-747. <https://doi.org/10.1112/S0024611503014266>

## Machine-readable companions

The authoritative structured companions are `MASTER_21_TASK_LEDGER.csv`, `CRITICAL_ERRATA_CATALOGUE.csv`, `BIBLIOGRAPHIC_PRIOR_NOTICE_MATRIX.csv`, `SEARCH_QUERY_LEDGER.csv`, `DEPENDENCY_PROPAGATION_EDGES.csv`, the frozen unresolved/variant ledgers, and `qa/MATHEMATICAL_CHECKS.json`.
