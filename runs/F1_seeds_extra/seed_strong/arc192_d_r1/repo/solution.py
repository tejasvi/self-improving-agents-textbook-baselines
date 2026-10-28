import sys

MOD = 998244353


def spf_table(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def run_dp(p, a, N, U):
    # sum over sequences e_1..e_N with values in [0,U], |e_{i+1}-e_i| = a_i,
    # of prod p^{e_i}  (mod MOD)
    pw = [1] * (U + 1)
    for v in range(1, U + 1):
        pw[v] = pw[v - 1] * p % MOD
    dp = pw[:]  # position 1: e_1 = v, weight p^v
    for i in range(N - 1):
        ai = a[i]
        if ai == 0:
            dp = [x * q % MOD for x, q in zip(dp, pw)]
            continue
        if ai > U:
            return 0
        left = [0] * ai + dp[:U + 1 - ai]   # dp[w - ai]
        right = dp[ai:] + [0] * ai          # dp[w + ai]
        dp = [(x + y) * q % MOD for x, y, q in zip(left, right, pw)]
    return sum(dp) % MOD


def solve_prime(p, a, N):
    S = sum(a)
    if S == 0:
        return 1
    g_full = run_dp(p, a, N, S)
    g_low = run_dp(p, a, N, S - 1)
    return (g_full - pow(p, N, MOD) * g_low) % MOD


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:N]]
    spf = spf_table(max(1000, max(A)))
    exps = {}
    for idx, x in enumerate(A):
        y = x
        while y > 1:
            q = spf[y]
            e = 0
            while y % q == 0:
                y //= q
                e += 1
            if q not in exps:
                exps[q] = [0] * (N - 1)
            exps[q][idx] = e
    ans = 1
    for p, a in exps.items():
        ans = ans * solve_prime(p, a, N) % MOD
    print(ans)


main()
