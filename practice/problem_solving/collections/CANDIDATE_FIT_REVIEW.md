# Initial Level C candidate fit review

This records the editorial review of 16 candidates for `medium_01` and
`hard_01`, using `src/scripts/prompts/level_c_candidate_fit.txt`. It judges
whether the underlying problem earns a Level C slot. It does not re-audit card
wording. The source statements and canonical explanations are available for
all 16; none is blocked on source readiness. The two rejected candidates were
removed from the active medium collection after this review.

`Accept` means the learner must infer a substantial approach or invariant and
the outline teaches a reusable idea. `Introductory` means a simpler card has a
deliberate foundation or contrast role. `Reject` means the remaining task is
chiefly implementation or a narrow trick with too little transferable reasoning
for a limited Level C cohort. These decisions are judgments, not scores.

| Card | Decision | Learner decision and collection contribution |
| --- | --- | --- |
| [Medium 2](medium_01/cards/problem-2.brief.md) | Introductory | Carry and unequal-length handling follow directly from reverse-order digits. It establishes a representation-aware addition baseline for the stronger contrast in 445. Place early. |
| [Medium 8](../../../problems/medium/8.md) | Reject | The source and faithful brief already prescribe the scan phases. The main remaining insight is a checked accumulation condition, useful implementation fluency but limited unaided approach selection. |
| [Medium 15](medium_01/cards/problem-15.brief.md) | Accept | The learner must derive sorting plus a monotone two-pointer search and prevent duplicate value triplets. This transfers to constrained k-sum search. |
| [Medium 47](medium_01/cards/problem-47.brief.md) | Accept | The learner must generate distinct value arrangements without treating equal occurrences as distinct outputs. Lexicographic enumeration and depth-level duplicate control offer reusable alternatives. |
| [Medium 106](medium_01/cards/problem-106.brief.md) | Accept | Root identification from postorder, partitioning by inorder position, and right-before-left reconstruction form a substantial interval invariant. |
| [Medium 199](medium_01/cards/problem-199.brief.md) | Introductory | The clarified brief defines the per-depth choice; the learner must select and justify a traversal that groups or prioritizes nodes at each depth. It is a gentle tree-view foundation, so place it early in that strand. |
| [Medium 207](medium_01/cards/problem-207.brief.md) | Accept | The learner must recognize prerequisite feasibility as directed-cycle absence and choose a way to establish it. This transfers to dependency scheduling. |
| [Medium 216](medium_01/cards/problem-216.brief.md) | Introductory | Increasing choices make combination generation unique, but the tiny fixed domain leaves little algorithmic pressure. It introduces the backtracking state before richer search problems. Place before 47 if retained. |
| [Medium 237](../../../problems/medium/237.md) | Reject | The missing predecessor and non-tail guarantee lead to one successor-substitution trick. After that deduction, the task is two pointer assignments; transfer beyond this mutation contract is narrow. |
| [Medium 306](medium_01/cards/problem-306.brief.md) | Accept | The learner must see that only the first two boundaries are free and every later term is forced, then preserve exact arithmetic and leading-zero rules. |
| [Medium 347](medium_01/cards/problem-347.brief.md) | Accept | The better-than-sorting bound creates a meaningful choice: exploit frequency as a bounded integer key. The counting-to-buckets insight transfers. |
| [Medium 375](medium_01/cards/problem-375.brief.md) | Accept | The learner must optimize a guarantee over the worse side of each guess and derive an interval recurrence. This is reusable minimax reasoning. |
| [Medium 445](medium_01/cards/problem-445.brief.md) | Accept | Forward-order digits require a way to process least-significant places first without reversing inputs. It adds a distinct representation constraint and contrasts with 2. |
| [Hard 4](hard_01/cards/problem-4.brief.md) | Accept | The logarithmic requirement forces a search over a valid median boundary, with a nontrivial partition invariant. |
| [Hard 10](hard_01/cards/problem-10.brief.md) | Accept | The learner must reason through repeat-or-skip matching states and full-string coverage. The recurrence and empty-prefix handling transfer to pattern DP. |
| [Hard 23](hard_01/cards/problem-23.brief.md) | Accept | The learner must exploit one sorted frontier per list and select the global minimum efficiently. The frontier invariant transfers to other multiway merges. |

Result: **11 accept, 3 introductory, 2 reject**. The 14 accepted and
introductory cards remain active. The two rejected card pairs were removed from
`medium_01`; their source problems remain in the repository. The introductory
cards need explicit placement and should be reconsidered as cohorts fill.
