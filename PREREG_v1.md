# Pre-registration v1: where do self-improvement gains come from?

Frozen before any main-campaign run. Date: 2026-10-23 (UTC). Infra and seeds as committed in ~/shi_eval
(seed_dgm commit ec73d48, seed_strong commit 923141e, splits_hard_v1.json sha256 050d161e...).

## Setting
- Tasks: LiveCodeBench hard problems with private tests <= 20 MB (282). Fixed shuffle (seed 20261024):
  S_small = 10, S_medium = 40 (selection set S, 50 tasks, DGM-style staging), F = 232 fresh tasks.
  F is never shown to any loop, diagnosis or human design step. F1 = first 116 of F (all-candidate scan).
- Task model: claude-haiku-5-5 (default thinking, no sampling params). Diagnosis model: claude-sonnet-5-5.
  Self-modification model: same as the agent's task model (DGM: the agent edits itself).
- Proxy shim applied to every harness: one tool call per response (2025 Claude behaviour).
- Grader: all public + private tests, 6 s per test, first failure stops. Agent wall-clock cap 600 s per task.
- Code: exp/dgm_lcb.py, exp/ladder.py, exp/dgm_prompts.py, infra/* as of the freeze (sha256 list in PREREG_v1.sha256).

## Arms (DGM seed unless noted)
- A  DGM loop, 40 generations x 2 attempts, 3 independent runs (seeds 1-3).
- B  Placebo loop (children are exact copies), same schedule, 3 runs.
- C1 Single-step children of the seed from log-free diagnoses (n = 24): prior only.
- C2 Single-step children of the seed from task-log diagnoses (n = 24): prior + feedback.
- D  Log-free chains: 10 steps, every change accepted without evaluation, 2 chains.
- E  DGM loop from the strong human seed, 2 runs; F-arm placebo from strong seed, 1 run; C1/C2 from strong seed (n = 16 each).
Reported "best" of a loop = DGM rule: highest S score among archive agents with full S evaluation.
Best-of-n for C1/C2 = highest S score (ties: earliest). Random member = expected value over members.

## Primary outcomes
1. Selection gain G_S = S(best) - S(seed); fresh gain G_F = F(best) - F(seed), paired over F tasks, 3 reps.
2. Inflation I = G_S - G_F, per run and pooled.
3. Gain ladder on F (relative to seed): L1 = mean C1 member, L2 = best-of-24 C1, L3 = mean C2 member,
   L4 = best-of-24 C2, L5 = arm A best. Contrasts: L1 (prior), L2-L1 (selection), L4-L2 (feedback),
   L5-L4 (iteration).
4. Placebo inflation: S(best placebo) - S(seed) (F gain is zero by construction).

## Hypotheses (directional)
H1 Placebo loops show S(best) - S(seed) > 0 (selection-only artifact), size within the order-statistics prediction.
H2 For arm A, G_S > G_F (inflation > 0) and G_F > 0 from the DGM seed.
H3 Prior dominates: L2 >= 0.8 * L5 on F (i.e. feedback + iteration add < 20% of the fresh gain).
H4 From the strong seed, G_F of all arms is within +-3 points of 0, while G_S > 0.
H5 Transfer: the fresh gain of arm-A best agents shrinks under models whose behaviour differs from the task
   model (non-thinking Haiku 4.5 and Sonnet 4.6), measured on F with the same harness.
Each hypothesis is reported as supported / not supported with 95% bootstrap CIs (tasks resampled, reps nested).
Results that contradict a hypothesis are reported as such; no hypothesis is dropped.

## Secondary
- Recursion (improver swap): same 16 diagnoses implemented on the seed's code by (a) the seed agent and
  (b) arm-A best agent as the editor; compare children on F.
- Process vs content: share of the fresh gain on tasks where the seed's failure was an empty patch.
- Cost per task of every harness (test-time compute) and gain per extra dollar.

## Stops
Proxy global cap raised in steps; hard stop at $2,500 all-in for this pre-registered campaign without a new
written plan. Any change to arms, splits or graders after the first main run is logged in DEVIATIONS.md.
