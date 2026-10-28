import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    P = int(data[idx]); idx += 1
    base = P + 1
    M = base ** K
    # digits of each state
    digits = []
    for s in range(M):
        d = []
        t = s
        for _ in range(K):
            d.append(t % base)
            t //= base
        digits.append(d)
    # weight of each digit position
    weights = [base ** j for j in range(K)]
    INF = float("inf")
    dp = [INF] * M
    dp[0] = 0
    for _ in range(N):
        C = int(data[idx]); idx += 1
        A = [int(data[idx + j]) for j in range(K)]
        idx += K
        # transition target for each state
        trans = [0] * M
        for s in range(M):
            d = digits[s]
            ns = 0
            for j in range(K):
                v = d[j] + A[j]
                if v > P:
                    v = P
                ns += v * weights[j]
            trans[s] = ns
        new_dp = dp[:]
        for s in range(M):
            cur = dp[s]
            if cur == INF:
                continue
            ns = trans[s]
            c = cur + C
            if c < new_dp[ns]:
                new_dp[ns] = c
        dp = new_dp
    target = M - 1  # all digits == P
    ans = dp[target]
    print(-1 if ans == INF else ans)


main()
