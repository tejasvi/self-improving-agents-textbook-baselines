import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    W = [int(x) for x in data[pos:pos + n]]; pos += n
    L = [0] * n
    R = [0] * n
    for i in range(n):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2
    q = int(data[pos]); pos += 1

    INF = 1 << 62
    M = 2 * n + 2  # coordinates 0..M

    # bestR[c]: min W over intervals with R == c
    bestR = [INF] * (M + 2)
    # bestL[c]: min W over intervals with L == c
    bestL = [INF] * (M + 2)
    for i in range(n):
        if W[i] < bestR[R[i]]:
            bestR[R[i]] = W[i]
        if W[i] < bestL[L[i]]:
            bestL[L[i]] = W[i]

    # gR[v] = min W over R_a < v
    gR = [INF] * (M + 2)
    cur = INF
    for v in range(M + 2):
        gR[v] = cur
        if bestR[v] < cur:
            cur = bestR[v]

    # sufL[v] = min W over L_b >= v
    sufL = [INF] * (M + 3)
    cur = INF
    for v in range(M + 1, -1, -1):
        if bestL[v] < cur:
            cur = bestL[v]
        sufL[v] = cur

    # hL[c] = min over b with L_b == c of W_b + gR[L_b]
    hL = [INF] * (M + 2)
    for b in range(n):
        val = W[b] + gR[L[b]]
        if val < hL[L[b]]:
            hL[L[b]] = val

    # sparse table for range min over hL
    size = M + 2
    table = [np.array(hL, dtype=np.int64)]
    k = 1
    while (1 << k) <= size:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append(np.minimum(prev[:-half], prev[half:]))
        k += 1
    table = [t.tolist() for t in table]

    def range_min(lo, hi):  # inclusive, lo <= hi
        length = hi - lo + 1
        j = length.bit_length() - 1
        t = table[j]
        a = t[lo]
        b = t[hi - (1 << j) + 1]
        return a if a < b else b

    def case1(s, t):
        # min W_a + W_b with R_a < L_s, R_a < L_b, R_t < L_b
        X = L[s]
        Y = R[t]
        best = INF
        M1 = max(X, Y + 1)
        if M1 <= M + 2:
            v = sufL[M1]
            if v < INF:
                g = gR[X]
                if g < INF and v + g < best:
                    best = v + g
        lo = Y + 1
        hi = X - 1
        if lo <= hi:
            v = range_min(lo, hi)
            if v < best:
                best = v
        return best

    out = []
    for _ in range(q):
        s = int(data[pos]) - 1
        t = int(data[pos + 1]) - 1
        pos += 2
        base = W[s] + W[t]
        if R[s] < L[t] or R[t] < L[s]:
            out.append(base)
            continue
        best = gR[min(L[s], L[t])]
        c2 = sufL[max(R[s], R[t]) + 1]
        if c2 < best:
            best = c2
        # 3-vertex path: s - a - t
        cand = best
        # 4-vertex path: s - a - b - t
        c4 = case1(s, t)
        c4b = case1(t, s)
        if c4b < c4:
            c4 = c4b
        if c4 < cand:
            cand = c4
        if cand >= INF:
            out.append(-1)
        else:
            out.append(base + cand)
    sys.stdout.write("\n".join(map(str, out)) + ("\n" if out else ""))


main()
