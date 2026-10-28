# solution.py
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
        # read n integers
        a = [int(next(it)) for _ in range(n)]
        best = -10**18
        cur = 0  # placeholder, will be set on first element
        for i, val in enumerate(a):
            if i == 0:
                cur = val
            else:
                if (val & 1) != (a[i-1] & 1):  # different parity with previous element
                    # we can either extend previous subarray or start new
                    cur = max(val, cur + val)
                else:
                    cur = val
            if cur > best:
                best = cur
        out_lines.append(str(best))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
