import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)
    total = pow(m, q, MOD)

    # S[k][w] (w = 0..m): number of assignments of suffix k..n-1 with all values <= w
    S = [None] * (n + 1)
    cur = [1] * (m + 1)
    S[n] = cur
    for i in range(n - 1, -1, -1):
        bi = b[i]
        if bi == -1:
            cur = [cur[w] * w % MOD for w in range(m + 1)]
        else:
            cur = [cur[w] if bi <= w else 0 for w in range(m + 1)]
        S[i] = cur

    # P[u] (u = 1..m+1): number of prefix assignments with all values >= u
    P = [1] * (m + 2)
    P[0] = 0
    P[m + 1] = 0
    result = 0
    for k in range(1, n):
        bi = b[k - 1]
        if bi == -1:
            for u in range(1, m + 1):
                P[u] = P[u] * (m - u + 1) % MOD
        else:
            for u in range(1, m + 1):
                if bi < u:
                    P[u] = 0
        Sk = S[k]
        s = 0
        for u in range(1, m + 1):
            e = P[u] - P[u + 1]
            if e:
                s += e * Sk[u - 1]
        result = (result + s) % MOD

    print((total + result) % MOD)


main()
