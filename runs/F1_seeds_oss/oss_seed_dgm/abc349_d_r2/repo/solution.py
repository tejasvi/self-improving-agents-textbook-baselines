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
        if cur == 0:
            # Largest power of two not exceeding remaining length
            remaining = R - cur
            size = 1 << (remaining.bit_length() - 1)
        else:
            lowbit = cur & -cur  # largest power of two dividing cur
            remaining = R - cur
            max_pow = 1 << (remaining.bit_length() - 1)
            size = lowbit if lowbit <= max_pow else max_pow
        intervals.append((cur, cur + size))
        cur += size
    out_lines = [str(len(intervals))]
    out_lines += [f"{l} {r}" for l, r in intervals]
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
