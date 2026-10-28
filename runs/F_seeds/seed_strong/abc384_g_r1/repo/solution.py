import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    A = [int(v) for v in data[pos:pos + n]]; pos += n
    B = [int(v) for v in data[pos:pos + n]]; pos += n
    k = int(data[pos]); pos += 1
    out = []
    for _ in range(k):
        x = int(data[pos]); y = int(data[pos + 1]); pos += 2
        # Sum over a in A[:x] of sum over b in B[:y] of |a-b|
        sb = sorted(B[:y])
        m = len(sb)
        pref = [0]
        s = 0
        for b in sb:
            s += b
            pref.append(s)
        total_b = s
        res = 0
        for a in A[:x]:
            c = bisect_left(sb, a)  # b < a for first c elements
            res += a * c - pref[c] + (total_b - pref[c]) - a * (m - c)
        out.append(res)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
