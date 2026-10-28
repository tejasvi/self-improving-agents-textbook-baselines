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
        # read n integers
        a = [int(next(it)) for __ in range(n)]
        best = -10**18
        prev_dp = None  # dp for previous element
        prev_parity = None
        for val in a:
            parity = val & 1  # 0 for even, 1 for odd (works for negatives too)
            # decide whether we can extend previous alternating subarray
            if prev_dp is not None and parity != prev_parity and prev_dp > 0:
                cur_dp = val + prev_dp
            else:
                cur_dp = val
            if cur_dp > best:
                best = cur_dp
            prev_dp = cur_dp
            prev_parity = parity
        out_lines.append(str(best))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
