import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    # prefix sums
    P = [0] * (n + 1)
    s = 0
    for i, a in enumerate(A):
        s += a
        P[i + 1] = s
    # sparse table: sp[k][i] = max(A[i .. i+2^k-1])
    sp = [A]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        h = 1 << (k - 1)
        cur = [x if x > y else y for x, y in zip(prev, prev[h:])]
        sp.append(cur)
        k += 1
    LOG = len(sp)

    out = []
    for K in range(n):
        l = r = K
        S = A[K]
        while True:
            # nearest left index j < l with A[j] >= S (or -1)
            p = l - 1
            for kk in range(LOG - 1, -1, -1):
                st = p - (1 << kk) + 1
                if st >= 0 and sp[kk][st] < S:
                    p -= 1 << kk
            jl = p
            # nearest right index j > r with A[j] >= S (or n)
            q = r + 1
            for kk in range(LOG - 1, -1, -1):
                if q + (1 << kk) <= n and sp[kk][q] < S:
                    q += 1 << kk
            jr = q
            nl, nr = jl + 1, jr - 1
            newS = P[nr + 1] - P[nl]
            l, r, S = nl, nr, newS
            can = (jl >= 0 and A[jl] < S) or (jr < n and A[jr] < S)
            if not can:
                break
        out.append(S)
    sys.stdout.write(" ".join(map(str, out)) + "\n")


main()
