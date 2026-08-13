# Cumulative source-error logbook through P11

The 1897 French diplomatic layer preserves every listed source form. The proposed correction, added hypothesis, or repaired proof belongs only to a visibly distinct critical or translation layer and must cite the corresponding certificate.

## W02-PE001 — W02, PDF 025 / L0024

- Region: lower half; line break déve-/veloppent
- Preserved source form: déveveloppent
- Critical form or repair not applied: développent
- Classification: `definite_1897_printed_error`.
- Proof status: `proved_philologically`. The 1897 line carry reads 'déve-' followed by 'veloppent', yielding the duplicated sequence 'déveveloppent'. French syntax and morphology require 'développent'; the error is nevertheless retained verbatim in the 1897 French layer.
- Editorial instruction: Preserve déveveloppent in the source-faithful French layer; any correction belongs only in a visibly separate critical note.
- Certificate: `W02-E025A; expanded_worker_returns/W02_PDF024-029_INTRODUCTION/PRINTED_ERRORS.csv`

## W03-PE001 — W03, PDF 035 / L0034

- Region: upper text block; conjugate-root display and immediately following prose
- Preserved source form: a + 1/(-1/B) = a - B; a - B
- Critical form or repair not applied: p + 1/(-1/B) = p - B; p - B
- Classification: `definite_1897_printed_letter_error`.
- Proof status: `proved_symbolically`. From x=p+1/A and conjugate(A)=-1/B, conjugation gives p+1/(-1/B)=p-B. The printed letter a is inconsistent with the established variable p.
- Editorial instruction: Preserve each printed a in the source-faithful layer. A correction to p belongs only in a visibly separate critical apparatus.
- Certificate: `expanded_worker_returns/W03_PDF030-037_CONTINUED_FRACTIONS/FORMULA_CHECKS.json#page035_letter_error`

## W03-PE002 — W03, PDF 035 / L0034

- Region: upper text block; sentence following conjugate-root display
- Preserved source form: compris entre 0 et 1
- Critical form or repair not applied: compris entre 0 et -1
- Classification: `definite_1897_printed_sign_error`.
- Proof status: `proved_symbolically`. Writing B=p+r with 0<r<1 gives p-B=-r, hence -1<p-B<0. The printed interval between 0 and 1 has the wrong sign.
- Editorial instruction: Preserve the printed positive 1. The algebraic interval correction is ledgered but not silently inserted.
- Certificate: `expanded_worker_returns/W03_PDF030-037_CONTINUED_FRACTIONS/FORMULA_CHECKS.json#page035_interval_sign_error`

## W03-PE003 — W03, PDF 037 / L0036

- Region: middle of page; second expression in les deux valeurs de x display
- Preserved source form: x = 3 - 1/A (printed as the full staircase reciprocal of the positive y expansion)
- Critical form or repair not applied: x = 3 - A
- Classification: `definite_1897_printed_formula_error`.
- Proof status: `proved_symbolically`. Substitution shows 3-A has zero residual in 3x^2-16x+18, whereas the printed 3-1/A has residual -4(-1+sqrt(10))/3 and is not a root.
- Editorial instruction: Preserve the printed reciprocal display. The following final continued fraction is separately transcribed as printed and evaluates to the corrected smaller root.
- Certificate: `expanded_worker_returns/W03_PDF030-037_CONTINUED_FRACTIONS/FORMULA_CHECKS.json#page037_correct_second_x;#page037_printed_second_x_error`

## W04-SE001 — W04, PDF 038 / L0037

- Region: § I theorem; first displayed quotient
- Preserved source form: Soient Fx et fx deux fonctions quelconques données; on aura, quels que soient x et h, [quotient]
- Critical form or repair not applied: Require f(x+h) != f(x) before forming the quotient.
- Classification: `substantive_1897_missing_hypothesis`.
- Proof status: `proved_exact_domain_counterexample`. For f identically zero, f(x+h)-f(x)=0 for every x,h, so the universally quantified quotient is undefined.
- Editorial instruction: Preserve the universal printed wording. Add the missing-domain condition only in a visibly separate critical or translated layer with this certificate.
- Certificate: `expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W04-SE001; expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/FORMULA_CHECKS.json#W04-MATH038B`

## W04-SE002 — W04, PDF 038 / L0037

- Region: § I final corollary sentence
- Preserved source form: ce qui démontre, a priori, l'existence des fonctions dérivées
- Critical form or repair not applied: No local normalization is sufficient; the universal claim must be translated literally with an erratum or replaced only in a separately reconstructed theorem with explicit hypotheses.
- Classification: `substantive_1897_false_mathematical_claim`.
- Proof status: `proved_exact_limit_counterexample`. For F(t)=|t|, f(t)=t, x=0, the quotient is |h|/h; the right limit is 1 and the left limit is -1.
- Editorial instruction: Preserve the printed claim in the source-faithful layer. A future critical layer must cite the |h|/h counterexample.
- Certificate: `expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W04-SE002; expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/FORMULA_CHECKS.json#W04-MATH038C`

## W04-SE003 — W04, PDF 038 / L0037

- Region: § I proof; transition from k=psi(P) to P=phi(k)
- Preserved source form: donc on doit avoir aussi P = phi(k)
- Critical form or repair not applied: Require injectivity of psi or specify an inverse branch before defining phi.
- Classification: `substantive_1897_invalid_inference`.
- Proof status: `proved_exact_logical_counterexample`. A noninjective ψ with ψ(0)=ψ(1)=0 cannot admit a single-valued φ satisfying P=φ(ψ(P)) for both P=0 and P=1.
- Editorial instruction: Preserve the printed inference. Any repair belongs only to separate critical apparatus and does not by itself repair the theorem.
- Certificate: `expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W04-SE003; expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/FORMULA_CHECKS.json#W04-MATH038D`

## W04-SE004 — W04, PDF 038 / L0037

- Region: § I proof; assertion that a nonconstant function with equal endpoint values has maxima and minima between them
- Preserved source form: à moins qu'elle ne reste constante entre ces limites [...] cette fonction aura, entre x et x+h, un ou plusieurs maxima et minima
- Critical form or repair not applied: Require continuity on the closed interval (or another hypothesis guaranteeing attainment of an interior extremum).
- Classification: `substantive_1897_missing_regularity_hypothesis`.
- Proof status: `proved_exact_extremum_counterexample`. A discontinuous function with equal endpoint values can be nonconstant while attaining no maximum and having no interior local extremum; continuity or another attainment hypothesis is required.
- Editorial instruction: Preserve the printed proof. A future critical layer must state a regularity hypothesis before invoking an extremum argument.
- Certificate: `expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W04-SE004; expanded_worker_returns/W04_PDF038-039_NOTES_ANALYSIS/FORMULA_CHECKS.json#W04-MATH038E`

## W05-SE001 — W05, PDF 040-041 / L0039-L0040

- Region: point 3, listed exceptions, and Dans le second cas continuation
- Preserved source form: A part les cas mentionnés ci-dessous [...] deux quelconques de ses racines étant connues, les autres s’en déduisent rationnellement.
- Critical form or repair not applied: The exception list is incomplete: a solvable primitive degree-8 affine-semilinear example has a nontrivial two-point stabilizer and is not covered by the printed congruence.
- Classification: `substantive_1897_too_restrictive_classification`.
- Proof status: `proved_exact_group_theoretic_counterexample`. AΓL(1,8) has order 168, derived-series orders 168,56,8,1, is two-transitive and primitive of degree 8, and has ordered two-point stabilizer order 3. Degree 8 fails the printed congruence exception. A fixed-field construction yields the required irreducible solvable degree-8 equation.
- Editorial instruction: Preserve the printed classification. Any correction belongs only in a visibly separate critical or translated layer with the degree-8 certificate.
- Certificate: `expanded_worker_returns/W05_PDF040-041_ALGEBRAIC_RESOLUTION_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W05-SE001; expanded_worker_returns/W05_PDF040-041_ALGEBRAIC_RESOLUTION_ANALYSIS/GROUP_THEORY_CHECKS.json#affine_semilinear_degree_8`

## W05-SE002 — W05, PDF 041 / L0040

- Region: second modular result immediately before Liouville’s corrective footnote
- Preserved source form: Au contraire, pour des degrés supérieurs, les équations modulaires ne peuvent s’abaisser.
- Critical form or repair not applied: The universal higher-degree impossibility is false for p=7 and p=11; the 1897 Liouville footnote itself records these exceptions.
- Classification: `substantive_1897_false_modular_impossibility`.
- Proof status: `proved_source_internal_and_exact_group_theoretic`. The corrective footnote on PDF 041 explicitly gives p=7 and p=11. Exact enumeration also finds index-7 and index-11 subgroups in PSL(2,7) and PSL(2,11), respectively.
- Editorial instruction: Preserve both the erroneous main-text sentence and Liouville’s historical correction. Do not absorb the footnote into the main text.
- Certificate: `expanded_worker_returns/W05_PDF040-041_ALGEBRAIC_RESOLUTION_ANALYSIS/MATHEMATICAL_ERROR_CERTIFICATES.md#W05-SE002; expanded_worker_returns/W05_PDF040-041_ALGEBRAIC_RESOLUTION_ANALYSIS/GROUP_THEORY_CHECKS.json#modular_exception_p7;#modular_exception_p11`

## W06-PE001 — W06, PDF 042 / L0041

- Region: second radical display and immediately following one-above/one-below sentence
- Preserved source form: x = psi x = nth_root( X / (x^n/Y) )
- Critical form or repair not applied: Critical reconstruction candidate: x = psi x = nth_root( Y / (X/x^n) )
- Classification: `definite_1897_printed_formula_error`.
- Proof status: `proved_symbolically`. For n=2, X=x^2+1, Y=3x, the fixed-point polynomial for the printed map has gcd 1 with F=x^2-3x+1, so neither root of F is fixed. A second exact example at x=1 gives both printed maps greater than x, refuting the claimed opposite-side behavior.
- Editorial instruction: Preserve the printed X numerator and x^n/Y denominator and preserve the following printed claim. Any symmetric correction belongs only in visibly separate critical apparatus with the exact certificate; the 1846 repetition is not a correcting variant.
- Certificate: `expanded_worker_returns/W06_PDF042-043_NUMERICAL_EQUATIONS/MATHEMATICAL_ERROR_CERTIFICATES.md#W06-PE001; expanded_worker_returns/W06_PDF042-043_NUMERICAL_EQUATIONS/FORMULA_CHECKS.json#W06-MATH001A-W06-MATH001D`

## W06-SE001 — W06, PDF 043 / L0042

- Region: identical strict inequalities and prescription of k at x=1
- Preserved source form: nX-xXprime > 0, nY-xYprime > 0; take k=(nX-xXprime) at x=1
- Critical form or repair not applied: For X=sum c_j x^j with c_j>=0, nX-xXprime=sum_{j<n}(n-j)c_jx^j; strict positivity on x>0 is equivalent to at least one positive coefficient below degree n. Require the analogous condition for Y.
- Classification: `substantive_1897_missing_nonvanishing_hypothesis`.
- Proof status: `proved_exact_polynomial_counterexample`. The exact coefficient identity proves nonnegativity. Strict positivity holds exactly when a lower-degree coefficient is positive; X=x^n gives zero identically. Thus the printed k is positive exactly under the added lower-degree-term hypothesis.
- Editorial instruction: Preserve both strict inequalities and the k prescription. A future critical or translated layer must state the missing nonvanishing or lower-degree-term hypothesis explicitly and cite the zero-k counterexample.
- Certificate: `expanded_worker_returns/W06_PDF042-043_NUMERICAL_EQUATIONS/MATHEMATICAL_ERROR_CERTIFICATES.md#W06-SE001; expanded_worker_returns/W06_PDF042-043_NUMERICAL_EQUATIONS/FORMULA_CHECKS.json#W06-MATH002; P06_REQUIRED_HYPOTHESIS_RECHECK.md; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH000A-W07-MATH000B`

## W07-SE001 — W07, PDF 046 / L0045

- Region: first historical footnote after Frobenius-root list
- Preserved source form: x^2+x+1=0 mod 2 is offered as an example showing the roots are not expressible by radicals because the ordinary quadratic formula reduces to 0/0.
- Critical form or repair not applied: A nontrivial root alpha satisfies alpha^3=1 and is itself a radical (a cube root of unity); 0/0 only shows degeneration of that formula in characteristic 2.
- Classification: `invalid_counterexample_to_nonradical_expressibility`.
- Proof status: `proved_exact_finite_field`. A root alpha of x^2+x+1 over F_2 satisfies alpha^3=1 and is a nontrivial cube root of unity; degeneration of the characteristic-zero quadratic formula to 0/0 is not a non-radicality proof.
- Editorial instruction: Preserve the complete footnote. Any correction belongs only in visibly separate critical/translation apparatus.
- Certificate: `expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/MATHEMATICAL_ERROR_CERTIFICATES.md#W07-SE001; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH001`

## W07-SE002 — W07, PDF 049 / L0048

- Region: Newton/Fermat reduction for (a+a_1 i)^19
- Preserved source form: a^{m(p-1)}=1 and a_1^{m(p-1)}=1 are used without a nonzero qualification.
- Critical form or repair not applied: Require a!=0 and a_1!=0 modulo p for these reductions; the chosen values a=-1,a_1=1 satisfy the missing condition.
- Classification: `missing_nonzero_hypotheses`.
- Proof status: `proved_exact_finite_field`. Fermat reduction u^{p-1}=1 requires u nonzero. Exact enumeration verifies the printed expansion for all 36 nonzero pairs and finds exactly 12 failures where exactly one of a,a_1 is zero; the selected pair (-1,1) is valid.
- Editorial instruction: Preserve the printed reductions and successful chosen pair; state the domain restriction only in a critical layer.
- Certificate: `expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/MATHEMATICAL_ERROR_CERTIFICATES.md#W07-SE002; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH011A;W07-MATH011B`

## W07-SE003 — W07, PDF 050 / L0049

- Region: preparation of F by removing gcd(F,Fprime)
- Preserved source form: The same derivative-gcd method as for ordinary equations is said always to remove repeated roots.
- Critical form or repair not applied: In characteristic p, Fprime may vanish identically; a p-th-root extraction branch is required before recursive squarefree reduction.
- Classification: `incomplete_squarefree_method_in_characteristic_p`.
- Proof status: `proved_exact_polynomial_counterexample`. For F=x^3-1=(x-1)^3 over F_3, Fprime=0 and F/gcd(F,Fprime)=1, losing the root. A p-th-root extraction branch is necessary.
- Editorial instruction: Preserve the historical method statement; attach the inseparability qualification only as critical apparatus.
- Certificate: `expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/MATHEMATICAL_ERROR_CERTIFICATES.md#W07-SE003; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH003`

## W07-SE004 — W07, PDF 050 / L0049

- Region: gcd procedure for integral solutions
- Preserved source form: Integral solutions are obtained from gcd(F,x^{p-1}-1).
- Critical form or repair not applied: This detects only nonzero residues. Use x^p-x for all residues, or test/remove x=0 separately.
- Classification: `zero_residue_omitted`.
- Proof status: `proved_exact_polynomial_counterexample`. For F=x, zero is an integral solution but gcd(x,x^{p-1}-1)=1. All residues are roots of x^p-x, or zero must be handled separately.
- Editorial instruction: Preserve x^{p-1}=1 in the French layer; any all-residue repair must be explicit.
- Certificate: `expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/MATHEMATICAL_ERROR_CERTIFICATES.md#W07-SE004; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH004`

## W07-SE005 — W07, PDF 050 / L0049

- Region: gcd procedure for imaginary solutions of order nu
- Preserved source form: Solutions of order nu are said to be given by gcd(F,x^{p^nu-1}-1).
- Critical form or repair not applied: The polynomial also contains every nonzero element of proper subfields whose degree divides nu; exact-degree isolation requires removal of proper-subfield factors (and separate zero handling).
- Classification: `proper_subfield_factors_not_removed`.
- Proof status: `proved_exact_polynomial_counterexample`. Every nonzero proper-subfield element satisfies x^{p^nu-1}=1 when its degree divides nu; for p=3,nu=2, the degree-one element 1 is included. Exact-degree factors must exclude proper subfields.
- Editorial instruction: Preserve the printed gcd prescription; defer a full exact-degree repair and propagation analysis to the bounded post-completion audit.
- Certificate: `expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/MATHEMATICAL_ERROR_CERTIFICATES.md#W07-SE005; expanded_worker_returns/W07_PDF044-053_NUMBER_THEORY/FORMULA_CHECKS.json#W07-MATH005`

## W08-PE001 — W08, PDF 058 / L0057

- Region: p=11 representative upper row
- Preserved source form: infinity, 1, 3, 5, 5, 9
- Critical form or repair not applied: infinity, 1, 3, 4, 5, 9
- Classification: `duplicated_representative_and_omitted_projective_point`.
- Proof status: `proved_exact_finite_set_group_and_secondary_witness`. The printed upper row contains six positions but only five distinct projective points; together with the lower row it duplicates 5 and omits 4. The 1846 publication supplies 4. Exact enumeration verifies the corrected partition of P^1(F_11), |PSL(2,11)|=660, and a matching stabilizer of order 60 and index 11.
- Editorial instruction: Preserve the second printed 5 in the 1897 French layer. Record 4 only in visibly separate critical/translation apparatus with the exact partition proof.
- Certificate: `expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/MATHEMATICAL_ERROR_CERTIFICATES.md#W08-PE001; expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/FORMULA_CHECKS.json#W08-MATH001-W08-MATH007; expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/figures/FIGURE_PROVENANCE.csv`

## W08-PE002 — W08, PDF 058 / L0057

- Region: sentence following p=5,7,11 modular-equation lowering
- Preserved source form: En toute rigueur, cette équation n’est pas possible dans les cas plus élevés.
- Critical form or repair not applied: En toute rigueur, cette réduction n’est pas possible dans les cas plus élevés.
- Classification: `editorial_word_substitution_attested_by_1846_and_1908_collation`.
- Proof status: `proved_by_direct_1846_and_1908_witness_collation`. The 1897 page visibly prints “équation”; the 1846 publication prints “réduction”; and Tannery’s 1908 collation explicitly reports that the 1897 edition substituted “équation” for the manuscript/Liouville “réduction”.
- Editorial instruction: Preserve “équation” in the 1897 French layer. Any “réduction” correction must be explicit critical apparatus.
- Certificate: `expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/MATHEMATICAL_ERROR_CERTIFICATES.md#W08-PE002; expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/EDITORIAL_COLLATION_NOTES.md; expanded_worker_returns/W08_PDF054-061_CHEVALIER_LETTER/figures/FIGURE_PROVENANCE.csv`

## W09-PE001 — W09, PDF 065 / L0064

- Region: Lemma II statement
- Preserved source form: en permutant dans celle fonction
- Critical form or repair not applied: en permutant dans cette fonction
- Classification: `definite_demonstrative_lexeme_error`.
- Proof status: `proved_by_primary_image_and_1846_collation`. The 1897 page visibly prints “celle fonction”; the 1846 publication prints “cette fonction”. The witnessed correction is confined to apparatus.
- Editorial instruction: Preserve “celle fonction” in the 1897 French layer; “cette fonction” belongs only in explicitly labelled critical or translation apparatus.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/PRINTED_ERRORS.csv; expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/EDITORIAL_COLLATION_NOTES.md`

## W09-PE002 — W09, PDF 071 / L0070

- Region: Chevalier/Liouville historical note to Proposition III
- Preserved source form: proprieté
- Critical form or repair not applied: propriété
- Classification: `definite_missing_diacritic_typographical_error`.
- Proof status: `proved_by_direct_primary_image_inspection`. The 1897 historical note visibly prints “proprieté” without the accent; the typographical error is retained in the diplomatic layer.
- Editorial instruction: Preserve “proprieté” in the 1897 French layer; normalize only in an explicitly labelled critical or translation layer.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/PRINTED_ERRORS.csv; expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/CHECKPOINT_CORRECTION_REPORT.md`

## W09-SE001 — W09, PDF 065-066 / L0064-L0065

- Region: Lemma III proof
- Preserved source form: The unique common root is said to be “sought”, and the root is therefore declared rational in V.
- Critical form or repair not applied: In K(V)[X], prove that the relevant gcd is X-a and use the Euclidean algorithm/Bézout identity to obtain a in K(V).
- Classification: `incomplete_proof_missing_gcd_bezout_step`.
- Proof status: `proved_by_exact_repair_or_counterexample`. Lemma III is repairable: in K(V)[X], the gcd of the original polynomial and the V-relation is X−a; a Bézout identity then expresses a rationally in V. The printed proof omits this decisive step, as the 1908 collation also reports.
- Editorial instruction: Preserve the printed proof. Put the complete gcd/Bézout argument only in critical apparatus and propagate its use to Proposition I.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE001`

## W09-SE002 — W09, PDF 069-070 / L0068-L0069

- Region: Proposition II statement and proof
- Preserved source form: After adjoining a root of an irreducible auxiliary equation, the group is unchanged or divides into p equal groups, although the prime-degree phrase defining p was deleted.
- Critical form or repair not applied: Let L be the original splitting field, M=K(r), E=L∩M, and H=Gal(L/E); then [G:H]=[E:K] divides [M:K]. The printed dichotomy follows when [M:K] is prime, not in arbitrary composite degree.
- Classification: `undefined_parameter_and_false_composite_degree_generality`.
- Proof status: `proved_by_exact_repair_or_counterexample`. The correct field-intersection identity gives subgroup index [L∩K(r):K], which divides the auxiliary degree. The printed unchanged-or-p-equal-groups dichotomy follows in the deleted prime-degree setting but is false for arbitrary composite degree; the exact degree-four counterexample is recorded.
- Editorial instruction: Preserve the 1897 theorem and historical note. State the field-intersection theorem only in a visibly distinct repaired layer.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE002`

## W09-SE003 — W09, PDF 070-071 / L0069-L0070

- Region: Proposition III
- Preserved source form: The revised theorem is printed without its proof (“On trouvera la démonstration”).
- Critical form or repair not applied: If M is the splitting field of the auxiliary equation and E=L∩M, then E/K is normal; hence H=Gal(L/E) is normal in G and the conjugate groups have the same substitution set.
- Classification: `missing_proof_requiring_normal_intersection_argument`.
- Proof status: `proved_by_exact_repair_or_counterexample`. With L and M the two splitting fields and E=L∩M, normality of E/K makes H=Gal(L/E) normal in G. This proves the revised Proposition III, but the 1897 text itself supplies no proof.
- Editorial instruction: Preserve the unproved printed statement and historical note; supply the normal-intersection proof only in critical apparatus.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE003`

## W09-SE004 — W09, PDF 073 / L0072

- Region: Proposition V Fourier/Lagrange resolvent argument
- Preserved source form: The proof adjoins the p-th root of one specifically displayed Fourier combination raised to p.
- Critical form or repair not applied: That selected coefficient may vanish. Choose a nonzero nontrivial Fourier coefficient; discrete Fourier inversion proves one exists for every nonconstant orbit.
- Classification: `proof_gap_selected_resolvent_can_vanish`.
- Proof status: `proved_by_exact_repair_or_counterexample`. The specifically displayed Fourier coefficient can vanish for a nonconstant orbit. Fourier inversion proves that some nontrivial coefficient is nonzero; the critical repair must select such a coefficient instead of assuming the displayed one.
- Editorial instruction: Preserve the displayed source formula; supply nonvanishing selection only in critical proof reconstruction.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE004`

## W09-SE005 — W09, PDF 075 / L0074

- Region: Proposition VI final inference
- Preserved source form: An irreducible prime-degree equation is said not to become reducible unless its group reduces to one permutation.
- Critical form or repair not applied: The inference requires the inherited roots-of-unity/Kummer normality context. Over Q, x^3-2 becomes reducible after adjoining its real cube root while a quadratic factor and residual group of order 2 remain.
- Classification: `false_unconditional_assertion_missing_kummer_normality_context`.
- Proof status: `proved_by_exact_repair_or_counterexample`. The unconditional final sentence fails for x^3−2 after adjoining one real cube root: the equation becomes reducible while the residual splitting group is C2. A roots-of-unity/Kummer normality context is required.
- Editorial instruction: Preserve the printed sentence. State the Kummer/normality hypotheses only in a critical layer and propagate the dependency to Proposition VII.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE005`

## W09-SE006 — W09, PDF 078 / L0077

- Region: Proposition VIII necessity argument
- Preserved source form: The affine substitution x_k↦x_{ak+b} is said never to leave two letters in place, with no exclusion of the identity.
- Critical form or repair not applied: Insert “nonidentity”: the identity a=1,b=0 fixes every letter; every nonidentity affine map fixes at most one point.
- Classification: `omitted_nonidentity_quantifier`.
- Proof status: `proved_by_exact_repair_or_counterexample`. The identity affine map fixes every letter, while each nonidentity affine map fixes at most one. The necessity argument is repaired by inserting the omitted nonidentity qualifier.
- Editorial instruction: Preserve the printed sentence; add the missing quantifier only in critical or expository apparatus. The theorem’s repaired argument remains valid.
- Certificate: `expanded_worker_returns/W09_PDF062-079_RADICALS_MEMOIR/MATHEMATICAL_ERROR_CERTIFICATES.md#W09-SE006`



## W10 — primitive-equations fragment (PDF080-091)

W10 contributes six definite printed formula/index errors and two missing identity qualifications. All eight forms remain verbatim in the diplomatic French layer. Tannery’s 1908 collation historically documents W10-PE001, PE002, PE003, and PE005; the 1846 publication already carries W10-PE006. Exact proofs and critical repairs are in `expanded_worker_returns/W10_PDF080-091_PRIMITIVE_EQUATIONS/MATHEMATICAL_ERROR_CERTIFICATES.md`.

- `W10-PE001`: The index declaration and Tannery collation establish that the second printed k_1 is a repetition for k_2.
- `W10-PE002`: Coordinate parallelism and Tannery collation establish psi(k_2) as the critical reading.
- `W10-PE003`: The source transformation acts on two indices; Tannery restores the missing separator and unchanged second coordinate.
- `W10-PE004`: Only k_1,k_2 are the established coordinate pair in this section; k_2,k_3 is not a map on the introduced domain.
- `W10-PE005`: Tannery’s two-coordinate affine formula is the unique form compatible with the finite-difference condition and correctly printed continuation.
- `W10-PE006`: The printed discriminant is exactly that of the fixed-point polynomial without the extra factor m and not of the printed polynomial.
- `W10-SE001`: The identity has a two-dimensional fixed space; every nonidentity affine map has empty fixed set or fixed dimension at most one.
- `W10-SE002`: The scalar subgroup includes identity; exactly p^2-2 nonidentity scalars move every nonzero vector while the group order remains p^2-1.

The printed word `ordre` on PDF088-090 denotes moved-letter count, not group-theoretic element order. This is protected negative coverage, not an erratum.
## W11 — historical table of contents and trailing backmatter (PDF092-096)

`W11-PE001` is a definite historical page-reference error. PDF092/L0091 visibly prints Arabic `1` beside `INTRODUCTION.`. The primary glyph is the same Arabic numeral used in the page-reference column; it is not roman `v`. The frozen page map and W02 metadata independently establish Picard’s Introduction as logical roman folios `v-x`, beginning at PDF024/L0023.

The diplomatic table retains `1`. A critical, GPT, or translation layer may display `v` only with an explicit erratum and the certificate in `expanded_worker_returns/W11_PDF092-096_BACKMATTER/ERRATA_AND_READING_CERTIFICATES.md`. Gutenberg’s generated page `1` is control repetition, not independent authority.

`W11-U001`, the printer’s four-digit job number on PDF093/L0092, remains an unresolved image reading and is not counted as a proved source error.
