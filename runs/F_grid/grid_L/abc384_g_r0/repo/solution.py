import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    A = [int(v) for v in data[idx:idx + n]]; idx += n
    B = [int(v) for v in data[idx:idx + n]]; idx += n
    k = int(data[idx]); idx += 1
    qs = []
    for qi in range(k):
        x = int(data[idx]); y = int(data[idx + 1]); idx += 2
        qs.append((x, y, qi))

    # Ranks: position of each element in sorted order of its own array (0-based).
    sortedA = sorted(range(n), key=A.__getitem__)
    sortedB = sorted(range(n), key=B.__getitem__)
    posA = [0] * n
    posB = [0] * n
    for p, i in enumerate(sortedA):
        posA[i] = p
    for p, j in enumerate(sortedB):
        posB[j] = p
    valsA = [A[i] for i in sortedA]
    valsB = [B[j] for j in sortedB]
    # Number of B-set elements (by sorted rank) with value < A_i is cutB[i]; similarly cutA.
    cutB = [bisect_left(valsB, a) for a in A]
    cutA = [bisect_left(valsA, b) for b in B]

    # Packed Fenwick: stores sum * SH + count, where SH = 2^17 > max count.
    SH = 17
    MASK = (1 << SH) - 1
    FA = [0] * (n + 1)  # A-set
    FB = [0] * (n + 1)  # B-set
    # Packed totals: sum*SH + count for each set.
    totA = 0
    totB = 0

    blk = max(1, int(2 * n / max(1, k) ** 0.5))
    qs.sort(key=lambda t: (t[0] // blk, t[1] if (t[0] // blk) & 1 == 0 else -t[1]))

    res = [0] * k
    curX = 0
    curY = 0
    cur = 0

    for x, y, qi in qs:
        while curX < x:
            # add A[curX] against current B-set
            a = A[curX]
            p = cutB[curX]
            s = 0
            while p > 0:
                s += FB[p]
                p &= p - 1
            cl = s & MASK
            sl = s >> SH
            tot = totB
            tc = tot & MASK
            ts = tot >> SH
            # sum |a-b| = a*cl - sl + (ts - sl) - a*(tc - cl)
            cur += a * (2 * cl - tc) + ts - 2 * sl
            # update FA
            v = (a << SH) + 1
            p = posA[curX] + 1
            while p <= n:
                FA[p] += v
                p += p & (-p)
            totA += v
            curX += 1
        while curY < y:
            b = B[curY]
            p = cutA[curY]
            s = 0
            while p > 0:
                s += FA[p]
                p &= p - 1
            cl = s & MASK
            sl = s >> SH
            tot = totA
            tc = tot & MASK
            ts = tot >> SH
            cur += b * (2 * cl - tc) + ts - 2 * sl
            v = (b << SH) + 1
            p = posB[curY] + 1
            while p <= n:
                FB[p] += v
                p += p & (-p)
            totB += v
            curY += 1
        while curX > x:
            curX -= 1
            a = A[curX]
            v = (a << SH) + 1
            p = posA[curX] + 1
            while p <= n:
                FA[p] -= v
                p += p & (-p)
            totA -= v
            p = cutB[curX]
            s = 0
            while p > 0:
                s += FB[p]
                p &= p - 1
            cl = s & MASK
            sl = s >> SH
            tot = totB
            tc = tot & MASK
            ts = tot >> SH
            cur -= a * (2 * cl - tc) + ts - 2 * sl
        while curY > y:
            curY -= 1
            b = B[curY]
            v = (b << SH) + 1
            p = posB[curY] + 1
            while p <= n:
                FB[p] -= v
                p += p & (-p)
            totB -= v
            p = cutA[curY]
            s = 0
            while p > 0:
                s += FA[p]
                p &= p - 1
            cl = s & MASK
            sl = s >> SH
            tot = totA
            tc = tot & MASK
            ts = tot >> SH
            cur -= b * (2 * cl - tc) + ts - 2 * sl
        res[qi] = cur

    sys.stdout.write("\n".join(map(str, res)) + "\n")


main()
