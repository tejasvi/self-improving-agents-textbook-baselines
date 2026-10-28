# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    L = int(data[0])
    R = int(data[1])
    intervals = []
    while L < R:
        if L == 0:
            # largest power of two not exceeding remaining length
            max_sz = 1 << ((R - L).bit_length() - 1)
        else:
            # largest power of two that divides L (alignment constraint)
            max_sz = L & -L
        # ensure the block does not exceed the remaining range
        while max_sz > R - L:
            max_sz >>= 1
        intervals.append((L, L + max_sz))
        L += max_sz
    out_lines = [str(len(intervals))]
    out_lines += [f"{l} {r}" for l, r in intervals]
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
