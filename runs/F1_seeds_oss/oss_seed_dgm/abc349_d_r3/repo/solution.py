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
        remaining = R - cur
        if cur == 0:
            # take the largest power of two not exceeding remaining
            size = 1 << (remaining.bit_length() - 1)
        else:
            lowbit = cur & -cur  # largest power of two dividing cur
            size = lowbit
            # shrink size until it fits into the remaining interval
            while size > remaining:
                size >>= 1
        intervals.append((cur, cur + size))
        cur += size
    out_lines = [str(len(intervals))]
    out_lines += [f"{l} {r}" for l, r in intervals]
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
