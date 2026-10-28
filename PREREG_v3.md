# Pre-registration v3: removing the remaining confounds

Frozen before any v3 run. Date: 2026-10-25 (UTC). Builds on PREREG_v1, PREREG_v2 and the first release of the paper
(Zenodo 10.5281/zenodo.23643513; code and data 10.5281/zenodo.23643515). Same tasks, grader v2, proxies and seeds.
Budget: the whole study stays under $10k all-in (Claude tokens included); about $8.5k is spent at this freeze. Hard
caps for v3: SWE machine proxy +$600, second-machine (LCB) proxy +$330, main proxy (redesign calls) +$30. Runs pause at
a cap; raising one needs a priced entry in DEVIATIONS.md.

## E1. SWE-bench at equal output budget
The released DGM agents request at most 4,096 output tokens per call; the textbook agent requests 16,000. E1 removes
this difference.
- Agents: dgm_init_16k and dgm_best_16k, the DGM's initial and reported best agents with one change (max_tokens=4096
  -> 16000 in llm_withtools.py; flagship/swe/r3_make_agents.sh), and moves, the textbook agent of v2, unchanged.
- One batch: all three agents start together, same task order, Claude Sonnet 4.5 (claude-sonnet-4-5@20250929), $10 per
  run, the DGM's harness with the clean setup step and the DGM's stock agent launch, as in v2's full run. Eight task
  containers per agent (v2 used 16), to reduce machine load; load, memory and kernel OOM events are logged
  (flagship/swe/r3_monitor.sh).
- Tasks: 65 fresh tasks drawn with Python random.Random(3).sample from the 246 fresh gold-resolvable tasks of v2
  (flagship/swe/r3_fresh65.json).
- Grading as in v2 (the DGM's report script; runs whose agent process ends before a patch is recorded count as
  unresolved). Sensitivity: patches present at an early ending graded as if kept, as in v2.
- H11: moves resolves at least as many tasks as dgm_best_16k minus 3 points (non-inferiority, paired bootstrap over
  tasks, 10,000 resamples, 95% interval); superiority (interval above 0) is reported as secondary.
- H12: dgm_best_16k - dgm_init_16k is reported with its interval; registered expectation: no significant improvement
  (two-sided, 5%).
- H13 (descriptive): moves - dgm_init_16k, the part of the textbook agent's lead that the output limit does not
  explain.
- Also reported: early-ending rate and exit codes per agent, OOM events, cost per run. Comparisons with v2's runs of
  dgm_init and dgm_best (4,096) on the same 65 tasks are exploratory, because they cross batches.

## E2. Random diagnosis with a clean request list
v2's list contained a request aimed at empty responses, the failure the first round had found. E2 repeats the test
without it.
- List: exp/random_moves_clean.py, the v2 list with three requests replaced (recover from responses with neither text
  nor a tool call; rerun when the solution file is unchanged; log each response's stop reason and usage) by three
  generic requests. No request mentions empty responses, output or token limits, stop reasons, or reruns after a
  missing solution.
- Loops: five clean random-diagnosis loops (seeds 11-15; launcher exp/dgm_lcb_rmclean.py, exp/dgm_lcb.py unchanged)
  and three DGM loops run at the same time (seeds 7-9), all with the settings of the v2 loops (Haiku 5.5 task and
  self-editing model, Sonnet 5.5 diagnosis, 40 generations, $0.25 and 600 s per task run, grader v2).
- Final evaluation in one common batch (all 232 fresh problems, two runs each, interleaved): the reported best agents
  of the five clean random-diagnosis loops, the three v2 random-diagnosis loops, the three new DGM loops and the six
  earlier DGM loops; the DGM seed; L.
- H14: the mean fresh gain of the clean random-diagnosis loops is at least the mean fresh gain of all nine DGM loops
  minus 3 points (non-inferiority; problems resampled with the loops fixed). Secondary: against the three same-time
  DGM loops; a Welch test at the level of loops is reported.

## E3. One-shot redesign without failure logs
- Five samples from Claude Opus 5.5 with v2's redesign prompt minus the logs of the five failed runs (agent summary,
  the DGM seed's code, the same task paragraph; exp/oneshot_redesign_logfree.py).
- Evaluation in one batch (all 232 fresh problems, two runs each): the five log-free redesigns, v2's five Opus
  redesigns (made from failure logs) and the DGM seed.
- H15: at least four of the five log-free redesigns raise the output cap above 4,096 tokens (as four of five log-based
  redesigns did), and their mean fresh gain is at least the mean of the log-based redesigns minus 3 points.

## Analysis rules
Primary contrasts are within one batch, so no seed adjustment is needed. Intervals are paired bootstraps over tasks
(10,000 resamples, 95%). Values are stored unrounded and rounded once for the paper. Results are reported whatever
the outcome. Every change after the first v3 run is logged in DEVIATIONS.md.
