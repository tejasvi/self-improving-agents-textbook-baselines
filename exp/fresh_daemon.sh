#!/bin/bash
# Periodically evaluate finished compiled children of v2 arms on F1 (116 fresh tasks). Stops when STOP_FRESH exists.
cd "$(dirname "$0")/.."
while [ ! -e STOP_FRESH ]; do
  for d in exps/v2_*; do
    e=$(basename $d)
    ./venv/bin/python -I exp/fresh_scan.py $e --stage fresh1 --which compiled --workers 8 >> results/fresh_daemon.log 2>&1
  done
  sleep 600
done
