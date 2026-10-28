#!/bin/bash
# Resume PREREG_v3 E1 on the SWE machine after a restart: proxy, monitors, then each agent's driver with the next
# attempt number (the driver runs only the instances that have no result yet). Skips agents whose driver is alive.
set -u
source "$HOME/shi_eval/flagship/swe/env.sh"
export HF_HUB_OFFLINE=1 HF_DATASETS_OFFLINE=1 TRANSFORMERS_OFFLINE=1
bash "$F/swe/start_proxy.sh" > /dev/null 2>&1
R=$F/runs_r3
[ -s "$R/monitor.pids" ] && [ -d "/proc/$(head -1 "$R/monitor.pids")" ] || bash "$F/swe/r3_monitor.sh" > /dev/null
for A in dgm_init_16k dgm_best_16k moves; do
  O=$R/r3_$A
  p=$(cat "$O/driver.pid" 2>/dev/null); [ -n "$p" ] && [ "$(cat /proc/$p/comm 2>/dev/null)" = python ] && continue
  K=$(ls "$O"/driver.a*.log 2>/dev/null | sed 's/.*driver\.a\([0-9]*\)\.log/\1/' | sort -n | tail -1); K=$((K + 1))
  setsid nohup "$PY" -I "$F/swe/run_flagship_v4.py" --keep-order --harness clean --agent-dir "$F/agents/$A/dgm" \
    --instances "$F/swe/r3_fresh65.json" --model claude-sonnet-4-5@20250929 --budget 10 --workers 8 --out "$O" \
    --attempt $K > "$O/driver.a$K.log" 2>&1 < /dev/null &
  echo $! > "$O/driver.pid"; echo "$(date -u +%FT%TZ) resumed $A as attempt $K pid $!" >> "$R/launch.log"
done
