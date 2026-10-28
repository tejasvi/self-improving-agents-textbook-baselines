import sys

MOD = 998244353


def factorize_small(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res


def walk_sum(es, p, S, L):
    # sum over sign patterns of walks v_1..v_N with all v in [L, S], weight p^(sum v)
    pw = [1] * (S + 1)
    for v in range(1, S + 1):
        pw[v] = pw[v - 1] * p % MOD
    dp = [pw[v] if v >= L else 0 for v in range(S + 1)]
    for e in es:
        if e == 0:
            dp = [x * w % MOD for x, w in zip(dp, pw)]
        else:
            if e > S:
                # no valid neighbours within range
                return 0
            pad = [0] * e
            left = pad + dp[:S + 1 - e]
            right = dp[e:] + pad
            dp = [(a + b) * w % MOD for a, b, w in zip(left, right, pw)]
        if L > 0:
            for u in range(min(L, S + 1)):
                dp[u] = 0
    return sum(dp) % MOD


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:n]]
    m = n - 1

    exps = {}
    for i, a in enumerate(A):
        for p, e in factorize_small(a).items():
            if p not in exps:
                exps[p] = [0] * m
            exps[p][i] = e

    ans = 1
    for p, es in exps.items():
        S = sum(es)
        f = (walk_sum(es, p, S, 0) - walk_sum(es, p, S, 1)) % MOD
        ans = ans * f % MOD
    print(ans % MOD)


main()
