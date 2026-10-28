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
        arr = [int(next(it)) for _ in range(n)]
        best = -10**18
        dp_prev = None
        for i, val in enumerate(arr):
            if i == 0:
                dp = val
            else:
                if (val & 1) != (arr[i-1] & 1):
                    # can extend or start new
                    dp = max(val, dp_prev + val)
                else:
                    dp = val
            dp_prev = dp
            if dp > best:
                best = dp
        out_lines.append(str(best))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
