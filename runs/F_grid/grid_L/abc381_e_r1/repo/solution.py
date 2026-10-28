import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    # 1-indexed prefix counts
    P1 = [0] * (n + 1)
    P2 = [0] * (n + 1)
    for i, ch in enumerate(s, 1):
        P1[i] = P1[i - 1] + (ch == '1')
        P2[i] = P2[i - 1] + (ch == '2')
    # nxt[i]: first slash position >= i (n+1 if none); prv[i]: last slash position <= i (0 if none)
    INF = n + 1
    nxt = [INF] * (n + 2)
    for i in range(n, 0, -1):
        nxt[i] = i if s[i - 1] == '/' else nxt[i + 1]
    prv = [0] * (n + 1)
    for i in range(1, n + 1):
        prv[i] = i if s[i - 1] == '/' else prv[i - 1]

    out = []
    idx = 3
    for _ in range(q):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        base1 = P1[L - 1]
        totR2 = P2[R]
        # g(m) = ones in [L,m-1] - twos in [m+1,R]; nondecreasing in m.
        # find first p in [L,R] with g(p) >= 0.
        lo, hi = L, R + 1
        while lo < hi:
            mid = (lo + hi) >> 1
            if (P1[mid - 1] - base1) - (totR2 - P2[mid]) >= 0:
                hi = mid
            else:
                lo = mid + 1
        p = lo
        best = 0
        if p <= R:
            m1 = nxt[p]
            if m1 <= R:
                # min = twos in [m1+1, R]
                k = totR2 - P2[m1]
                if k > best:
                    best = k
        if p - 1 >= L:
            m0 = prv[p - 1]
            if m0 >= L:
                # min = ones in [L, m0-1]
                k = P1[m0 - 1] - base1
                if k > best:
                    best = k
        out.append(2 * best + 1 if (p <= R and nxt[p] <= R) or (p - 1 >= L and prv[p - 1] >= L) else 0)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
