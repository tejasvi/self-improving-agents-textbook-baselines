# Write your solution here. Read from stdin, write to stdout.
import sys

def max_alternating_parity_subarray_sum(arr):
    # DP similar to Kadane but can only extend when parities differ
    best = -10**9  # overall maximum
    cur = None
    for i, val in enumerate(arr):
        if i == 0:
            cur = val
        else:
            if (val & 1) != (arr[i-1] & 1):  # different parity with previous element
                # we can extend previous subarray, but only if it improves sum
                if cur > 0:
                    cur = cur + val
                else:
                    cur = val
            else:
                cur = val
        if cur > best:
            best = cur
    return best

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
        ans = max_alternating_parity_subarray_sum(arr)
        out_lines.append(str(ans))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
