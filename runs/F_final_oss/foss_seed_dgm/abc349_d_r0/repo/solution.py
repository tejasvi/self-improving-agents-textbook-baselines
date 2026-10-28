# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    L = int(data[0])
    R = int(data[1])
    intervals = []
    cur = L
    while cur < R:
        remaining = R - cur
        if cur == 0:
            # Largest power of two not exceeding remaining
            max_len = 1 << (remaining.bit_length() - 1)
        else:
            # lowbit of cur
            max_len = cur & -cur
        # Ensure the block does not exceed the remaining length
        while max_len > remaining:
            max_len >>= 1
        intervals.append((cur, cur + max_len))
        cur += max_len
    # Output
    out_lines = [str(len(intervals))]
    out_lines += [f"{l} {r}" for l, r in intervals]
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
