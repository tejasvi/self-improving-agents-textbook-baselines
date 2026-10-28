#!/bin/bash
# Resume the v3 jobs on the second machine after a restart (run as user lcb in ~/shi_eval): start the proxies, then
# restart every v3 loop that has not reached its last generation and has no live process. Loops resume from state.json
# (a finished child is kept; an unfinished one is redone).
set -u
cd "$HOME/shi_eval" || exit 2
bash box_tools/lcb_start_proxies.sh > /dev/null 2>&1
LOG=results/r3/launch.log
alive() { [ -s "$1" ] && [ -d "/proc/$(cat "$1")" ] && [ "$(cat /proc/$(cat "$1")/comm 2>/dev/null)" = python ]; }
for E in v4_RMC_s11 v4_RMC_s12 v4_RMC_s13 v4_RMC_s14 v4_RMC_s15 v4_A_dgm_s7 v4_A_dgm_s8 v4_A_dgm_s9; do
  G=$(./venv/bin/python -I -c "import json,sys; print(json.load(open(sys.argv[1]))['generation'])" exps/$E/state.json 2>/dev/null || echo 0)
  [ "$G" -ge 40 ] && continue
  alive exps/$E/run.pid && continue
  case $E in v4_RMC_*) S=exp/dgm_lcb_rmclean.py;; *) S=exp/dgm_lcb.py;; esac
  setsid nohup ./venv/bin/python -I $S $E >> exps/$E/run.log 2>&1 < /dev/null &
  echo $! > exps/$E/run.pid; echo "$(date -u +%FT%TZ) resumed $E at generation $G pid $!" >> "$LOG"
done
# E3 evaluation batch (resumes: the batch skips jobs already in its results file)
if [ -e results/F_redesign_lf.log ] && [ "$(wc -l < results/F_redesign_lf.jsonl 2>/dev/null || echo 0)" -lt 5104 ] && ! alive results/F_redesign_lf.pid; then
  H=$HOME/shi_eval/harness; A="lf_seed_dgm=$H/seed_dgm"
  for i in 0 1 2 3 4; do A="$A lf_opuslf_r$i=$H/redesign/opuslf_r$i lf_opus_r$i=$H/redesign/opus_r$i"; done
  setsid nohup ./venv/bin/python -I exp/eval_interleaved.py F_redesign_lf fresh 2 claude-haiku-5-5 24 $A >> results/F_redesign_lf.log 2>&1 < /dev/null &
  echo $! > results/F_redesign_lf.pid; echo "$(date -u +%FT%TZ) resumed F_redesign_lf pid $!" >> "$LOG"
fi
# E2 common batch (resumes: eval_interleaved skips jobs already in results/F_final_r3.jsonl)
if [ -e results/F_final_r3.log ] && [ "$(wc -l < results/F_final_r3.jsonl 2>/dev/null || echo 0)" -lt 8816 ] && ! alive results/F_final_r3.pid; then
  setsid nohup ./venv/bin/python -I exp/r3_final_batch.py 48 >> results/F_final_r3.log 2>&1 < /dev/null &
  echo $! > results/F_final_r3.pid; echo "$(date -u +%FT%TZ) resumed F_final_r3 pid $!" >> "$LOG"
fi
