#!/bin/bash
# PREREG_v3 E2 and E3 on the second machine (run as user lcb in ~/shi_eval): start the proxies, set the v3 cap
# (ledger spend + $330), write the configs of five clean random-diagnosis loops (seeds 11-15) and three DGM loops
# (seeds 7-9) with the v3-loop settings, start all eight, then make the five log-free Opus redesigns.
# Parallelism: 8 task workers per loop (v2/v3 loops used 12) so that the eight loops use 64 sandboxes on 64 threads.
set -u
cd "$HOME/shi_eval" || exit 2
bash box_tools/lcb_start_proxies.sh
SPENT=$(./venv/bin/python -I -c "import json,sys; print(round(sum(json.loads(l).get('usd') or 0 for l in open(sys.argv[1])), 2))" ledger/ledger.jsonl)
CAP=$(./venv/bin/python -I -c "import sys; print(round(float(sys.argv[1]) + 330, 2))" "$SPENT")
echo "$CAP" > ledger/global_cap.txt
mkdir -p results/r3; LOG=results/r3/launch.log
echo "$(date -u +%FT%TZ) ledger spent $SPENT; cap set to $CAP" >> "$LOG"
for s in 11 12 13 14 15; do
  ./venv/bin/python -I exp/make_cfg.py v4_RMC_s$s mode=randommove seed=$s task_timeout=600 task_workers=8 grader=v2 > /dev/null || exit 3
done
for s in 7 8 9; do
  ./venv/bin/python -I exp/make_cfg.py v4_A_dgm_s$s mode=dgm seed=$s task_timeout=600 task_workers=8 grader=v2 > /dev/null || exit 3
done
for s in 11 12 13 14 15; do
  E=v4_RMC_s$s; setsid nohup ./venv/bin/python -I exp/dgm_lcb_rmclean.py $E > exps/$E/run.log 2>&1 < /dev/null &
  echo $! > exps/$E/run.pid; echo "$(date -u +%FT%TZ) started $E pid $!" >> "$LOG"
done
for s in 7 8 9; do
  E=v4_A_dgm_s$s; setsid nohup ./venv/bin/python -I exp/dgm_lcb.py $E > exps/$E/run.log 2>&1 < /dev/null &
  echo $! > exps/$E/run.pid; echo "$(date -u +%FT%TZ) started $E pid $!" >> "$LOG"
done
tail -9 "$LOG"
