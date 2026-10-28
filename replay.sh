#!/bin/bash
# Regenerate the paper's numbers (paper/numbers.tex, paper/numbers_v2.tex, paper/numbers_v3.tex), its generated tables
# (paper/tab_*.tex), the summary files in results/ and the figure (paper/fig1.pdf, paper/fig1.png) from the shipped
# result files.
# Needs Python 3 with numpy, scipy and matplotlib. Usage: bash replay.sh
set -euo pipefail
cd "$(dirname "$0")"
root=$(pwd -P)
# The analysis scripts find the project at ~/shi_eval; a temporary home directory points that name at this tree.
home=$(mktemp -d "${TMPDIR:-/tmp}/replay_home.XXXXXX")
ln -s "$root" "$home/shi_eval"
export HOME="$home" OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
export SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH:-1792886400}
PY=${PYTHON:-python3}
# first round, then the second-round chain in the order of analysis/run_chain_v2.sh, then the third round
for s in quirk seed_at_k summary \
         summary_v2 summary_v2_loops summary_v2_models l_at_k loops_vs_L oss_grid_summary oss_redesign_summary \
         flagship_summary flagship_sensitivity referee_v2_stats referee_v2_stats_r2 misc_v2 h5_both_loops \
         k45_grid_summary aux_v2 numbers_v2 figure1 \
         r3_swe r3_redesign_lf r3_loops numbers_v3; do
  echo "== analysis/$s.py"
  "$PY" -I -B "analysis/$s.py" > /dev/null
done
unlink "$home/shi_eval"
echo "Done. To compare every file with the shipped copies: sha256sum -c --quiet SHA256SUMS"
echo "(The temporary home directory $home holds only a matplotlib cache and can be deleted.)"
