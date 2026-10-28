#!/bin/bash
# Re-run the second-round analysis chain: result summaries (results/*.json), then paper/numbers_v2.tex and
# paper/tab_*.tex, then Figure 1. Run from anywhere; paths resolve from this file's location.
# results/swe_kill_scan.json and results/pilot_empty.json come from analysis/swe_kill_scan.py and analysis/pilot_empty.py,
# which read agent chat logs that are not part of the release; the chain reads their stored outputs.
set -euo pipefail
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
PY="${PYTHON:-python3}"
for s in summary_v2 summary_v2_loops summary_v2_models l_at_k loops_vs_L oss_grid_summary oss_redesign_summary \
         flagship_summary flagship_sensitivity referee_v2_stats referee_v2_stats_r2 misc_v2 h5_both_loops \
         k45_grid_summary aux_v2 numbers_v2 figure1; do
  echo "== $s"
  "$PY" analysis/$s.py > /dev/null
done
echo "chain done"
