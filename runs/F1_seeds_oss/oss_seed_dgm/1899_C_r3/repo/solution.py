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
        a = [int(next(it)) for _ in range(n)]
        best = -10**18  # overall best
        cur = -10**18   # best sum of subarray ending at previous position
        for i, val in enumerate(a):
            if i > 0 and (a[i] % 2) != (a[i-1] % 2):
                # can extend previous subarray
                cur = max(val, cur + val)  # either start new or extend
            else:
                # must start new at current position
                cur = val
            if cur > best:
                best = cur
        out_lines.append(str(best))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
