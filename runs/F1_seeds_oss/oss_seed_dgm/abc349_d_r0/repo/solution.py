# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    L, R = map(int, data)
    intervals = []
    cur = L
    while cur < R:
        # maximum block size aligned at cur
        if cur == 0:
            # any power of two works, choose largest not exceeding remaining length
            max_pow = (R - cur).bit_length() - 1
            size = 1 << max_pow
        else:
            # lowbit of cur (largest power of two dividing cur)
            lowbit = cur & -cur
            size = lowbit
            # ensure size does not exceed remaining length
            while size > R - cur:
                size >>= 1
        intervals.append((cur, cur + size))
        cur += size
    # output
    out_lines = [str(len(intervals))]
    out_lines += [f"{l} {r}" for l, r in intervals]
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
