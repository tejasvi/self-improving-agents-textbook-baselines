import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    P = [0] * (n + 1)
    s = 0
    for i, a in enumerate(A):
        s += a
        P[i + 1] = s

    # sparse table: sp[k][i] = max(A[i .. i + 2^k - 1])
    sp = [A]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        h = 1 << (k - 1)
        sp.append(list(map(max, prev[:-h], prev[h:])))
        k += 1
    LOG = len(sp)

    res = []
    for K in range(n):
        l = K
        r = K
        S = A[K]
        while True:
            moved = False
            # extend left: absorb all of [p, l-1] that are < S
            p = l
            for kk in range(LOG - 1, -1, -1):
                step = 1 << kk
                q = p - step
                if q >= 0 and sp[kk][q] < S:
                    p = q
            if p < l:
                S = P[r + 1] - P[p]
                l = p
                moved = True
            # extend right: absorb all of [r+1, q-1] that are < S
            q = r + 1
            for kk in range(LOG - 1, -1, -1):
                step = 1 << kk
                if q + step <= n and sp[kk][q] < S:
                    q += step
            if q > r + 1:
                S = P[q] - P[l]
                r = q - 1
                moved = True
            if not moved:
                break
        res.append(S)
    sys.stdout.write(" ".join(map(str, res)) + "\n")


main()
