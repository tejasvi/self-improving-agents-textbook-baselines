# Write your solution here. Read from stdin, write to stdout.
import sys
from collections import Counter

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        cnt = Counter(arr)
        total = 0
        for v in cnt.values():
            total += v * (v - 1) // 2
        # add pairs (1,2)
        total += cnt.get(1, 0) * cnt.get(2, 0)
        out_lines.append(str(total))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
