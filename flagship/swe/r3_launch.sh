#!/bin/bash
# PREREG_v3 E1 (run on the SWE VM): dgm_init_16k, dgm_best_16k and moves on the 65 fresh tasks of swe/r3_fresh65.json,
# one batch: same task order for all agents (--keep-order), all three started together, claude-sonnet-4-5@20250929,
# clean setup, the DGM's stock agent launch, $10 per run, 8 task containers per agent. The VM proxy's global cap is set
# to the VM ledger's spend so far plus $600. Tags r3_<agent>.
set -u
source "$HOME/shi_eval/flagship/swe/env.sh"
R="$F/runs_r3"; mkdir -p "$R"; L="$HOME/shi_eval/ledger"
SPENT=$("$PY" -I -c "import json,sys; print(round(sum(json.loads(l).get('usd') or 0 for l in open(sys.argv[1])), 2))" "$L/ledger.jsonl")
CAP=$("$PY" -I -c "import sys; print(round(float(sys.argv[1]) + 600, 2))" "$SPENT")
echo "$CAP" > "$L/global_cap.txt"
echo "$(date -u +%FT%TZ) VM ledger spent $SPENT; cap set to $CAP" >> "$R/launch.log"
for A in dgm_init_16k dgm_best_16k moves; do
  O="$R/r3_${A}"; [ -e "$O" ] && { echo "exists: $O"; exit 1; }; mkdir -p "$O"
  setsid nohup "$PY" -I "$F/swe/run_flagship_v4.py" --keep-order --harness clean --agent-dir "$F/agents/$A/dgm" \
    --instances "$F/swe/r3_fresh65.json" --model claude-sonnet-4-5@20250929 --budget 10 --workers 8 --out "$O" \
    > "$O/driver.a0.log" 2>&1 < /dev/null &
  echo $! > "$O/driver.pid"
  echo "$(date -u +%FT%TZ) started $A pid $!" >> "$R/launch.log"
done
cat "$R/launch.log"
