# Write your solution here. Read from stdin, write to stdout.
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
        ans = 0
        for cnt in freq.values():
            ans += cnt * (cnt - 1) // 2
        ans += freq.get(1, 0) * freq.get(2, 0)
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
