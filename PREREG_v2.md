# Pre-registration v2: do self-improving harnesses find anything beyond textbook engineering?

Frozen before any v2 run. Date: 2026-10-23 (UTC). Builds on PREREG_v1 (same tasks, grader v2, proxy, seeds).
Budget: the whole study (v1 + v2, all-in incl. model tokens) stays under $10k; pause and review at $8.5k.

## Baselines that require no self-improvement (the "random search vs NAS" analogues)
B1 Textbook-move grid (no search). The hand-written seed decomposes into four file-level moves applied to the DGM
   seed: E editor (tools/edit.py: view/create/str_replace/insert), B shell (tools/bash.py: non-interactive, closed stdin,
   timeouts), L model loop (llm_withtools.py: 16k output budget, every tool call answered, one re-prompt after
   truncation, 40-turn cap), P workflow prompt (coding_agent.py: samples, brute force, timing). All 16 subsets are
   evaluated (seed = {}, hand-written seed = {E,B,L,P}); plus the cap-only seed (v1).
B2 Random-diagnosis loops (search without diagnosis). The DGM loop unchanged except that each diagnosis is replaced by
   one statement drawn uniformly from a fixed list of 20 generic improvement requests (exp/random_moves.py, written
   before any run, none mentions the output cap or token limits by name).
B3 One-shot expert redesign (diagnosis without search). claude-opus-5-5 receives the seed's code and the logs of 5
   failed selection-set runs once and returns a revised harness; no evaluation feedback; 5 independent samples.
B4 Lineage ablation. For the reported best agent of each v1 DGM loop, re-evaluate the agent with each lineage edit
   removed (all other edits applied in order; edits that no longer apply are reported as such).

## Generality
G-model: DGM loops (3) and a placebo loop (1) with gpt-oss-120b as task and self-editing model (diagnosis Sonnet 5.5),
   20 generations (cost/latency), via the second proxy.
G-search: 3 loops with HGM-style parent selection (Thompson sampling on clade pass/fail counts, as in HGM) on the same
   seed/tasks as v1.
G-power: 3 more DGM loops and 3 more placebo loops (seeds 4-6), same settings as v1.

## Published systems (flagship test)
P1 DGM / SWE-bench Verified: DGM initial agent vs DGM's reported best agent (released lineage patches applied to the
   released initial code) vs initial + textbook moves (str_replace editor; adequate output budget; robust loop) vs
   initial + moves + test-based retry matched to the best agent's cost. Tasks: the 300 Verified tasks outside DGM's
   200-task evaluation set (fresh) and DGM's 60 selection tasks (replication). Task models: claude-haiku-4-5 (closest
   available regime to DGM's retired claude-3.5-sonnet) and claude-haiku-5-5. One run per task per agent.
P2 HGM's released best agent on the same tasks and models.
P3 DGM / Polyglot: initial vs DGM's best polyglot agent vs initial + moves; gpt-oss-120b (stand-in for o3-mini) and
   claude-haiku-5-5; all 225 tasks, reported separately for the 166 never used in DGM's selection.
P4 ADAS (MGSM, DROP, GPQA, MMLU): best-by-validation discovered agent vs CoT-SC with the number of samples matched to
   the agent's model calls; claude-haiku-5-5; full test sets.

## Hypotheses (95% paired bootstrap CIs; non-inferiority margin 3 points)
H6 Best textbook-move combination >= best v1 DGM-loop agent - 3 points on F (fresh), at lower cost per task.
H7 Mean fresh gain of random-diagnosis loops >= mean of v1 DGM loops - 3 points.
H8 Best of 5 one-shot redesigns >= best v1 DGM-loop agent - 3 points; the mean redesign >= mean v1 loop best - 3.
H9 In each loop-best lineage, at most two edits carry >= 80% of the fresh gain (leave-one-out).
H10 For each published system, seed + textbook moves (+ matched retry) >= flagship best - 3 points on its fresh tasks.
Reported whatever the outcome; contradicting results are reported as such.

## Measurement
Fresh evaluation: F (232) for LCB agents, 2 runs per problem for B1-B4 finalists; references as in v1 (pooled seed runs,
plus same-batch seed runs evaluated alongside each new arm to control drift). All changes after the first v2 run go to
DEVIATIONS.md.
