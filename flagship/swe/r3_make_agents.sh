#!/bin/bash
# PREREG_v3 E1 agents (run on the SWE VM): dgm_init_16k and dgm_best_16k are copies of the DGM's initial and reported
# best agents with one change, max_tokens=4096 -> max_tokens=16000 in llm_withtools.py (the tool-calling request);
# nothing else differs. Refuses to overwrite and checks that exactly one line changed.
set -eu
source "$HOME/shi_eval/flagship/swe/env.sh"
for A in dgm_init dgm_best; do
  S="$F/agents/$A/dgm"; D="$F/agents/${A}_16k/dgm"
  [ -d "$S" ] || { echo "missing $S"; exit 1; }
  [ -e "$F/agents/${A}_16k" ] && { echo "exists: $F/agents/${A}_16k"; exit 1; }
  n=$(grep -c 'max_tokens=4096,' "$S/llm_withtools.py")
  [ "$n" = "1" ] || { echo "$A: expected one max_tokens=4096 line, found $n"; exit 1; }
  mkdir -p "$F/agents/${A}_16k"
  cp -a "$S" "$D"
  sed -i 's/max_tokens=4096,/max_tokens=16000,/' "$D/llm_withtools.py"
  c=$(diff -r --exclude=__pycache__ --exclude=.git "$S" "$D" | grep -c '^[<>]' || true)
  [ "$c" = "2" ] || { echo "$A: unexpected diff size $c"; exit 1; }
  diff -r --exclude=__pycache__ --exclude=.git "$S" "$D" || true
  echo "$A -> ${A}_16k ok"
done
