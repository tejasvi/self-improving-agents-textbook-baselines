import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    q = int(data[1 + n])
    pos = 2 + n
    # c[s] = s - h(s), h(s) = first index j with A[j] >= 2*A[s]
    c = [s - bisect_left(A, 2 * A[s]) for s in range(n)]
    sp = [c]
    p = 1
    while (1 << p) <= n:
        prev = sp[-1]
        half = 1 << (p - 1)
        cur = [min(prev[i], prev[i + half]) for i in range(n - (1 << p) + 1)]
        sp.append(cur)
        p += 1
    LOG = len(sp)
    out = []
    INF = 1 << 60
    for _ in range(q):
        L = int(data[pos]) - 1
        R = int(data[pos + 1]) - 1
        pos += 2
        D = R - L + 1
        maxk = D // 2
        K = 0
        mn = INF
        for p in range(LOG - 1, -1, -1):
            k2 = K + (1 << p)
            if k2 > maxk:
                continue
            m2 = sp[p][L + K]
            if m2 > mn:
                m2 = mn
            if D + m2 >= k2:
                K = k2
                mn = m2
        out.append(K)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
