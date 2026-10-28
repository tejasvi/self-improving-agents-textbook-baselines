#!/bin/bash
# PREREG_v3 E1 monitors (run on the SWE VM): load every 60 s, memory every 10 s, kernel OOM-killer lines as they occur.
# Writes under $HOME/shi_eval/flagship/runs_r3/. PIDs of the three samplers go to monitor.pids.
set -u
R="$HOME/shi_eval/flagship/runs_r3"; mkdir -p "$R"
[ -s "$R/loadlog.tsv" ] || echo -e "utc\tload1\tload5\tload15" > "$R/loadlog.tsv"
[ -s "$R/memlog.tsv" ] || echo -e "utc\tused_mib\tavailable_mib\ttotal_mib" > "$R/memlog.tsv"
setsid nohup bash -c 'while true; do read -r a b c _ < /proc/loadavg; echo -e "$(date -u +%Y-%m-%dT%H:%M:%SZ)\t$a\t$b\t$c" >> "$0/loadlog.tsv"; sleep 60; done' "$R" < /dev/null > /dev/null 2>&1 &
echo $! > "$R/monitor.pids"
setsid nohup bash -c 'while true; do free -m | awk -v t="$(date -u +%Y-%m-%dT%H:%M:%SZ)" "/^Mem:/ {print t \"\t\" \$3 \"\t\" \$7 \"\t\" \$2}" >> "$0/memlog.tsv"; sleep 10; done' "$R" < /dev/null > /dev/null 2>&1 &
echo $! >> "$R/monitor.pids"
setsid nohup bash -c 'sudo journalctl -k -f -o short-iso 2>/dev/null | grep --line-buffered -i -E "out of memory|oom-kill|killed process" >> "$0/oom.log"' "$R" < /dev/null > /dev/null 2>&1 &
echo $! >> "$R/monitor.pids"
echo "monitors started: $(tr '\n' ' ' < "$R/monitor.pids")"
