import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        pos += 1
        a = list(map(int, data[pos:pos + n]))
        pos += n
        pref = [0] + list(accumulate(a))
        best = 0
        for k in range(1, n + 1):
            if n % k:
                continue
            # block sums: pref[(j+1)k] - pref[jk]
            starts = pref[0:n:k]
            ends = pref[k::k]
            sums = [e - s for s, e in zip(starts, ends)]
            d = max(sums) - min(sums)
            if d > best:
                best = d
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
