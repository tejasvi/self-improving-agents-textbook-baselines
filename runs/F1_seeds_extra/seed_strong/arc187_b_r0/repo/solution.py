import sys
from array import array
from operator import mul, sub

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    B = [int(v) for v in data[2:2 + n]]
    P = 998244353

    # L_k[t] = #ways prefix 1..k has all values > t  (t in 0..m)
    # R_k[t] = #ways suffix k+1..n has all values <= t
    # f = 1 + #{cut k in 1..n-1 : min prefix > max suffix}
    # cut count = sum_t L_k[t] * (R_k[t] - R_k[t-1]) over t in 1..m
    q = 0
    for b in B:
        if b == -1:
            q += 1
    total = pow(m, q, P)

    coefL = [m - t for t in range(m + 1)]
    L = [1] * (m + 1)
    stored = [None] * n  # stored[k] for k in 1..n-1
    for k in range(1, n):
        b = B[k - 1]
        if b == -1:
            L = [x * c % P for x, c in zip(L, coefL)]
        else:
            # values > t allowed iff b > t, i.e. t < b; zero for t >= b
            L[b:] = [0] * (m + 1 - b)
        stored[k] = array('q', L)

    ans = 0
    R = [1] * (m + 1)
    coefR = list(range(m + 1))
    for k in range(n - 1, 0, -1):
        b = B[k]  # position k+1 (1-indexed) -> index k
        if b == -1:
            R = [x * c % P for x, c in zip(R, coefR)]
        else:
            # values <= t allowed iff b <= t; zero for t < b
            R[:b] = [0] * b
        Lk = stored[k]
        diff = list(map(sub, R[1:], R[:-1]))  # for t=1..m
        ans = (ans + sum(map(mul, Lk[1:], diff))) % P
    ans = (ans + total) % P
    print(ans)

main()
