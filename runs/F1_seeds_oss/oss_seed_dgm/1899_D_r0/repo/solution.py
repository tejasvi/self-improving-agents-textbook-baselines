# Solution for Yarik and Musical Notes problem
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        freq = {}
        for _ in range(n):
            a = int(next(it))
            freq[a] = freq.get(a, 0) + 1
        total = 0
        # pairs with equal a
        for cnt in freq.values():
            total += cnt * (cnt - 1) // 2
        # pairs (1,2)
        cnt1 = freq.get(1, 0)
        cnt2 = freq.get(2, 0)
        total += cnt1 * cnt2
        out_lines.append(str(total))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
