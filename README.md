# Code and data for "Do Self-Improving Coding Agents Beat Textbook Baselines?"

This archive accompanies the paper "Do Self-Improving Coding Agents Beat Textbook Baselines? Evidence from a Darwin
Gödel Machine Port and Two Published Systems" by Tejasvi S. Tomar (DOI 10.5281/zenodo.23719814,
https://doi.org/10.5281/zenodo.23719814). Its own DOI is 10.5281/zenodo.23719813
(https://doi.org/10.5281/zenodo.23719813), and the same files are on GitHub at
https://github.com/tejasvi/self-improving-agents-textbook-baselines (tag v3). It contains the code of the study, the
three pre-registrations, the change log, the per-task results of every evaluation in the paper, and the scripts that
compute the paper's numbers from those results.

## Regenerating the paper's numbers

    bash replay.sh
    sha256sum -c --quiet SHA256SUMS

`replay.sh` runs the analysis scripts in a fixed order. They write the result summaries in `results/*.json`, the macro
files `paper/numbers.tex`, `paper/numbers_v2.tex` and `paper/numbers_v3.tex`, the table bodies `paper/tab_*.tex` and
Figure 1 (`paper/fig1.pdf` and `paper/fig1.png`). The second command then compares every file with its shipped copy;
it prints nothing when all files match.

On one core the replay takes less than a minute. It needs Python 3 with numpy, scipy and matplotlib; the shipped files
were computed with Python 3.14.4, numpy 2.5.4, scipy 1.18.1 and matplotlib 3.11.2. With another matplotlib version,
the two figure files are not byte-identical.

Because the analysis scripts look for the project in `~/shi_eval`, `replay.sh` runs them with a temporary home
directory in which that name points to this archive. It first runs the first-round scripts `analysis/quirk.py`,
`analysis/seed_at_k.py` and `analysis/summary.py`, then the second-round scripts in the order given in
`analysis/run_chain_v2.sh`, which ran them during the study. Last come the third-round scripts `analysis/r3_swe.py`,
`analysis/r3_redesign_lf.py`, `analysis/r3_loops.py` and `analysis/numbers_v3.py`.

Most numbers in the paper are LaTeX macros, defined in `paper/numbers.tex` for the first round, in
`paper/numbers_v3.tex` for the third round and in `paper/numbers_v2.tex` for everything else; task counts, budgets and
the cost totals in the appendix are written directly in the paper source. To find the result file and field behind a
macro, look it up in `analysis/summary.py`, `analysis/numbers_v2.py` or `analysis/numbers_v3.py`.

## Terms

The study ports the Darwin Gödel Machine (DGM) to competitive-programming problems from LiveCodeBench. In the DGM's
self-improvement loop, a coding agent edits its own code, starting from a seed agent. Before each edit, a diagnosis
model reads the log of a failed task and proposes a change. Each loop scores new agents on a selection set S of 50
problems, evaluated in two stages called `small` and `medium`. An edited agent enters the archive when it scores at
least the seed's score minus 0.1, and parents of new edits are picked from the archive. A loop reports as its best
agent the archive agent with the highest score on S. Another 232 problems form the fresh set F, split into the halves
F1 and F2; no loop saw a fresh problem. A placebo loop runs the same schedule but keeps exact copies of the parent
agent instead of edits.

Three other terms recur below. H1 to H15 are the paper's pre-registered hypotheses. The study's first grader had a bug
and was replaced by a corrected grader. A compute-matched baseline runs the seed several times per problem and submits
the first solution that passes the problem's sample tests.

The textbook moves are four standard changes to the DGM seed: an editor that replaces exact strings (E), a shell that
runs commands without waiting for input (B), a model loop with an adequate output budget (L) and a workflow prompt (P).
The engineered seed is the DGM seed with all four moves, written directly, without search. A one-shot redesign is a
single model call that rewrites the DGM seed from five failure logs, without any evaluation. A lineage ablation removes
the edits of a loop agent one at a time.

Three variants of the loop appear in the second round. A random-diagnosis loop replaces each diagnosis by a request
drawn from a fixed list of 20 generic requests. HGM-style parent selection picks the parent by Thompson sampling over
the passes and failures of each archive agent and its descendants. In the improver swap, the seed and an agent found
by a loop receive the same diagnoses, and each implements them on the seed's code.

The paper also re-tests two published systems: the SWE-bench agents released with the DGM, and ADAS (Automated Design
of Agentic Systems), which searches for agent designs written as code. SWE-bench Verified is a set of software tasks,
each a repository issue with hidden tests; the DGM reported results on this benchmark for its released agents.

The third round addresses three remaining questions. E1 reruns the DGM's SWE-bench agents with the same output budget
as the textbook agent, which is the DGM's initial agent with three textbook moves. E2 repeats the random-diagnosis
loops with a clean request list, which contains no request aimed at the failure that the first round found. E3 makes
one-shot redesigns without failure logs.

## Contents

| Path | Contents |
|---|---|
| `PREREG_v1.md`, `PREREG_v2.md`, `PREREG_v3.md` | The three pre-registrations, as frozen |
| `PREREG_v1.sha256`, `PREREG_v2.sha256`, `PREREG_v3.sha256` | SHA-256 hashes taken at each freeze, of the pre-registration and of the code frozen with it |
| `DEVIATIONS.md` | The change log, with every change and decision after the first pre-registration |
| `exp/` | The DGM loop ported to LiveCodeBench, its variants, and the scripts that built and evaluated the baselines |
| `infra/` | LiveCodeBench task access, sandboxed grading, the model proxy with dollar caps and the task runner |
| `harness/` | The seed agents, the combinations of textbook moves, the one-shot redesigns and the lineage-ablation variants |
| `exps/` | One directory per loop, with its configuration, its archive, and the edit and the results of every agent |
| `runs/` | The solution files behind the stored sample-test results of the compute-matched baselines |
| `results/` | Per-task results of every evaluation batch and the summaries computed from them |
| `ledger/` | The model-call records of one batch |
| `flagship/` | The SWE-bench tests of the DGM's released agents |
| `adas_p4/` | The re-evaluation of the agents that ADAS discovered |
| `ext/adas/` | The archives that ADAS released, unmodified |
| `analysis/` | The scripts that compute the summaries, the paper's macros, the tables and Figure 1 |
| `paper/` | The LaTeX source of the paper |
| `replay.sh` | The command that regenerates the numbers |

## Agents

The DGM seed (the DGM's coding agent as ported) is in `harness/seed_dgm`, the engineered seed in `harness/seed_strong`,
and the DGM seed with only its output cap raised in `harness/seed_dgm_cap16k`. For the 16 combinations of the textbook
moves applied to the DGM seed, see `harness/grid/<moves>`, where `none` is the DGM seed itself.

Each redesign model made five one-shot redesigns, which are in `harness/redesign/<model>_r<i>`. Each model's prompt
(`<model>_prompt.txt`) and raw responses (`<model>_r<i>.raw.txt`) are in the same directory. Redesigns made from
failure logs of gpt-oss-120b carry the prefix `opusoss`.

The lineage-ablation variants of three first-round loop agents are in `harness/ablate/`, one directory per agent, each
with a `manifest.json` that lists the patches applied in each variant. The semantic ablation in
`v2_A_dgm_s3__g024_0/semantic_cap4096` is the agent of loop 3 with only its raised output cap reverted.

## Loops

Each loop directory `exps/<loop>/` contains the loop's `config.json` and, for loops with an archive, `state.json`, the
archive and `dgm_metadata.jsonl` (one line per generation). For every agent, `agents/<id>/meta.json` records its
parent, the diagnosis and the selection result, and `agents/<id>/patch.diff` is its edit relative to its parent.

Task runs are recorded one per line in `agents/<id>/evals/<stage>.jsonl`. The stages `small` and `medium` form the
selection set S, and `fresh1` and `fresh2` cover F1 and F2. Repeated runs on S are in `sel`. Files ending in
`.v2.jsonl` were graded again with the corrected grader.

The full code of each loop's reported best agent is in `agents/<id>/code/`. To rebuild any other agent, apply the
patches along its lineage to the seed. This table maps the loop directories to the paper.

| Loop directories | In the paper |
|---|---|
| `v2_A_dgm_s1` to `v2_A_dgm_s3` | First-round DGM loops 1 to 3 |
| `v2_B_placebo_s1` to `v2_B_placebo_s3` | First-round placebo loops |
| `v2_E_strong_dgm_s1`, `v2_E_strong_dgm_s2`, `v2_E_strong_placebo_s1` | Loops from the engineered seed (H4) |
| `v2_C1_nolog`, `v2_C2_single`, `v2_C3_nohint`, `v2_D_chain1`, `v2_D_chain2`, `v2_E_strong_C1_nolog`, `v2_E_strong_C2_single` | Single edits and chains of edits from a seed (H3) |
| `v2_A_nohint_s1`, `v2_A_nohint_s2` | Loops without hint prompts (exploratory) |
| `v2_R_swap` | Improver swap |
| `A_dgm_s1`, `A_dgm_s2`, `B_placebo_s1`, `E_strong_dgm_s1`, `E_strong_dgm_s2` | Loops graded by the first grader (grader analysis) |
| `v3_A_dgm_s4` to `v3_A_dgm_s6`, `v3_B_placebo_s4` to `v3_B_placebo_s6` | Second-round DGM loops and placebo loops |
| `v3_RM_s1` to `v3_RM_s3` | Random-diagnosis loops |
| `v3_H_hgm_s1` to `v3_H_hgm_s3` | Loops with HGM-style parent selection |
| `v3_K45_dgm_s1`, `v3_K45_dgm_s2`, `v3_K45_placebo_s1` | Loops with Claude Haiku 4.5 |
| `v3_O_dgm_s1` to `v3_O_dgm_s3`, `v3_O_placebo_s1` | Loops with gpt-oss-120b |
| `v4_RMC_s11` to `v4_RMC_s15` | Clean random-diagnosis loops (third round, E2) |
| `v4_A_dgm_s7` to `v4_A_dgm_s9` | DGM loops run at the same time as the clean random-diagnosis loops (E2) |

## Result files

Each line of a per-task result file describes one task run, with these fields.

- `agent`, `task` and `rep` name the agent, the problem and the repetition.
- `passed` is the verdict, and `grade` gives the number of tests run and the first failing test.
- `empty` marks a run that wrote no solution.
- `agent_timed_out` marks a run that reached the time limit, and `agent_rc` is the exit status of the agent process.
- `wall` is the run time in seconds and `usd` the model cost.
- `calls`, `inp` and `out` count the model calls and the input and output tokens.

| Files in `results/` | Part of the paper |
|---|---|
| `F_seeds.v2.jsonl`, `F1_seeds_extra*.jsonl`, `X_*.jsonl`, `summary.json`, `seed_at_k.json`, `quirk.json`, `retro.json` | Section "Where a loop's gain comes from", Figure 1 and the appendix "First-round details" |
| `F_grid.jsonl`, `l_at_k.json`, `loops_vs_L.json`, `grid_empty.json` | Textbook moves in the section "Second-round results" |
| `F_redesign.jsonl`, `redesign_caps.json` | One-shot redesigns |
| `F_ablate.jsonl`, `F1_cap16k.jsonl` | Lineage ablation and the seed with only its output cap raised |
| `F_final.jsonl`, `F_final_manifest.json`, `summary_v2_loops.json` | The common batch that evaluated all loop agents together (table of loop agents) |
| `F_final_k45.jsonl`, `F1_seeds_k45.jsonl`, `F_grid_k45.jsonl`, `k45_*.json` | Other task models, Claude Haiku 4.5 |
| `F_final_oss.jsonl`, `F1_seeds_oss.jsonl`, `F_grid_oss.jsonl`, `F_redesign_oss.jsonl`, `oss_*.json` | Other task models, gpt-oss-120b |
| `summary_v2.json`, `summary_v2_models.json`, `h5_both_loops.json`, `referee_v2_stats*.json`, `misc_v2.json`, `pilot_empty.json` | Hypothesis tests and further statistics |
| `flagship_summary.json`, `flagship_sensitivity.json`, `swe_kill_scan.json` | Section "Published systems", SWE-bench |
| `r3_swe.json` | Third round, E1 |
| `F_final_r3.jsonl`, `F_final_r3_manifest.json`, `r3_loops.json` | Third round, E2 |
| `F_redesign_lf.jsonl`, `r3_redesign_lf.json` | Third round, E3 |

`results/public_pass_cache.json` contains the sample-test result of each solution file in `runs/` that the
compute-matched baselines use.

`ledger/ledger.jsonl` contains the model-call records of one batch, the Claude Haiku 4.5 runs of the DGM seed in
`results/F_final_k45.jsonl`. Each record keeps the fields that `analysis/referee_v2_stats.py` reads, plus cost and token
counts.

## SWE-bench

The four SWE-bench agents are in `flagship/agents/`. `dgm_init/` is the DGM's initial agent in the form in which the
DGM's search ran it, and `dgm_best/` is the reported best agent, rebuilt by applying the six patches of its lineage
(combined in `flagship/agents/dgm_best_lineage.diff`). `moves/` adds three textbook moves to the initial agent, and
`moves_retry/` adds a retry to `moves/`. Hashes of the last two are listed in
`flagship/swe/agents_moves_manifest.sha256`. Check them from inside `flagship/agents/`.

`flagship/swe/run_flagship_v4.py` runs one agent through the DGM's own SWE-bench harness, in which the agent works
inside the task's container. `flagship/swe/dgm_harness_proxy_clean.py` is that harness with the clean setup step,
which removes pytest caches and hidden test files after the DGM's own setup step.

Two instance lists in `flagship/swe/` define the tasks, and both keep only tasks whose reference patch resolves them.
`fresh_gold.json` covers the SWE-bench Verified tasks outside the DGM's 200 tasks, and `dgm60_gold.json` covers the
DGM's selection tasks. The checks behind these lists are recorded in `gold_validation.json`,
`excluded_build_failures.json` and `leak_check.json`.

For each agent, `flagship/runs_full/flag_<agent>_s45/results.jsonl` has one line per task run. A run counts as an early
ending if its agent process ended before a patch was recorded. In the same directory, `regrade.json` lists the runs
graded again after an evaluation timeout or error, and `run_meta.a0.json` records the agent's commit, the model and the
settings. Final patches are in `predictions/*/all_preds.jsonl`, and the patches that were present when runs ended early
were graded separately (`flagship/runs_full/sensitivity/`). The table `flagship/runs_full/final_report_runs.tsv` lists
every run of the four agents with its outcome, cost, early ending and mean machine load; the one-minute load samples are
in `loadlog.tsv` in the same directory.

## ADAS

`adas_p4/adas_port.py` evaluates the agents of ADAS's released archives with a newer model and changes only the model
call. The per-question results, a summary and the code of each evaluated agent are in `adas_p4/full/`, where
`final_table.json` compares the discovered agents with matched chain-of-thought sampling (CoT-SC). ADAS's own archives
are in `ext/adas/`.

## Third round

The clean request list is in `exp/random_moves_clean.py`, and `exp/dgm_lcb_rmclean.py` runs a random-diagnosis loop
with it. The redesigns without failure logs come from `exp/oneshot_redesign_logfree.py`. On the second machine,
`exp/r3_box_launch.sh` started the E2 loops and the E3 redesigns, and `exp/r3_box_resume.sh` resumed them after each
restart. The common batch of E2 was run by `exp/r3_final_batch.py`.

The five redesigns without failure logs are in `harness/redesign/opuslf_r<i>`, with their raw responses in
`opuslf_r<i>.raw.txt`. Their prompt, `opuslf_prompt.txt`, contains only the agent summary, the DGM seed's code and the
task paragraph.

The five clean random-diagnosis loops are in `exps/v4_RMC_s11` to `exps/v4_RMC_s15`, and the three DGM loops that ran
at the same time are in `exps/v4_A_dgm_s7` to `exps/v4_A_dgm_s9`. These directories have the layout of the other loops.

For E1, `flagship/swe/r3_make_agents.sh` makes the agents `dgm_init_16k` and `dgm_best_16k` from the DGM's two agents.
It raises one output limit in `llm_withtools.py` from 4,096 to 16,000 tokens and checks that nothing else changes. E1
used the 65 fresh tasks listed in `flagship/swe/r3_fresh65.json`. The same directory has the scripts that start the run
(`r3_launch.sh`), log load, memory and out-of-memory events (`r3_monitor.sh`), resume the run after a restart
(`r3_swe_resume.sh`) and grade the patches of early-ended runs (`r3_sens_grade.py`).

During E1, `flagship/swe/r3_sitecustomize.py` answered the requests that swebench sends to raw.githubusercontent.com
from `flagship/swe/raw_github_cache.json`. That file is a cache of requirement files from the SWE-bench repositories,
fetched once with the same URLs. The URLs were recorded in `r3_urls.json` by `r3_record_urls.py`, and
`r3_check_specs.py` checks that every test specification builds from the cache.

For each E1 agent, `flagship/runs_r3/r3_<agent>/` contains `results.jsonl` (one line per task run), `summary.json`,
`run_meta.a3.json`, one status file per task run in `status/` and the final patches in `predictions/*/all_preds.jsonl`.
Patches present at early endings were graded separately, with the results in `flagship/runs_r3/sensitivity/`. The starts
and restarts of the run are recorded in `launch.log`, the machine's load and memory in `loadlog.tsv` and `memlog.tsv`,
and the kernel's out-of-memory events in `oom.log`.

The registered and exploratory statistics of E1, E2 and E3 are computed by `analysis/r3_swe.py`, `analysis/r3_loops.py`
and `analysis/r3_redesign_lf.py`. `analysis/numbers_v3.py` writes the third round's macros to `paper/numbers_v3.tex`
from their outputs and the load logs of both SWE-bench rounds.

## Material not in this archive

The LiveCodeBench problem statements and tests are not included, and `data/lcb/` contains only the problem IDs and the
splits. Wherever a shipped file quoted a statement, the statement is replaced by a placeholder that names the problem
and its question id. They can be restored from LiveCodeBench by title or id; they are needed to run agents or to grade
solutions again, but not for the replay.

The transcripts of the agent runs, of the self-modification steps and of the SWE-bench runs are not included. Per-run
results, edits and final patches are included.

Three scripts read material that is not included. The DGM's released run logs are read by `analysis/retro.py`, and
the chat logs of the SWE-bench runs and of the second pilot by `analysis/swe_kill_scan.py` and
`analysis/pilot_empty.py`. Their outputs `results/retro.json`, `results/swe_kill_scan.json` and
`results/pilot_empty.json` are shipped, and the replay reads them as inputs.

`adas_p4/adas_port.py` imports ADAS's modules from a checkout of the ADAS repository at commit 2702bee8, which is not
included.

## Running the experiments

Running the experiment code requires the project in `~/shi_eval`, a Python environment with the agents'
requirements, the LiveCodeBench data and bubblewrap for the sandboxes. Model calls go through `infra/llm_proxy.py`,
which checks per-run and global dollar caps. For the SWE-bench runs, Docker and swebench 2.1.0 are also required.

## Notes on the archived files

The shipped files are identical to the files used in the study, apart from the changes listed here.

- Home-directory paths are written as `~/shi_eval`. Python code resolves them with `os.path.expanduser`, for which
  an `os` import was added to three helper scripts in `adas_p4/`. The two shell scripts in `exp/` change to the
  archive root.
- The cloud project id is replaced by the placeholder `__CLOUD_PROJECT__` in `infra/llm_proxy.py`,
  `infra/translate.py` and `flagship/swe/llm_proxy_cache.py`.
- LiveCodeBench statements and excerpts of them are replaced by placeholders in the three prompts
  `harness/redesign/*_prompt.txt` and in one program output stored in `results/X_claude-sonnet-4-6.jsonl`.
- `analysis/seed_at_k.py` loads the problem index only when it is present. Its cache of sample-test results uses paths
  relative to the archive root as keys, and `results/public_pass_cache.json` was converted to such keys.
- `ledger/ledger.jsonl` is a subset of the full call ledger, which has about two million records.
- The creation date inside `paper/fig1.pdf` is set to 2026-10-25 00:00 UTC, the date that `replay.sh` passes to
  matplotlib.
- Files hashed in `PREREG_v2.sha256` or `PREREG_v3.sha256` are shipped unchanged, so that both hash files verify.
  Their comments keep the original wording, which names the SWE-bench machine in `flagship/swe/run_flagship_v4.py`.
- In all other files, comments and docstrings were edited so that machine names are neutral, dated decisions are
  called "decision", and no comment refers to review notes outside this archive. In `flagship/runs_r3/oom.log` the
  machine's host name is replaced by `swe-machine`. One summary string in `analysis/referee_v2_stats.py` and
  `results/referee_v2_stats.json` was changed in the same way.
- `DEVIATIONS.md` differs from the working log, and its header lists the differences.
- `PREREG_v1.sha256` lists five files that were changed after the first freeze: `exp/dgm_lcb.py`, `exp/make_cfg.py`,
  `infra/lcb.py`, `infra/llm_proxy.py` and `infra/run_task.py`. `DEVIATIONS.md` records each change. All files listed
  in `PREREG_v2.sha256` and `PREREG_v3.sha256` match.
- The run records in `flagship/runs_full/*/run_meta.a0.json` also record the one-line change to the model name that
  the DGM agents received at run time.

## License

The code is licensed under the Apache License 2.0, given in `LICENSE`. The data, the texts and the paper source are
licensed under CC BY 4.0. `NOTICE` lists the files derived from the Darwin Gödel Machine and from ADAS.
