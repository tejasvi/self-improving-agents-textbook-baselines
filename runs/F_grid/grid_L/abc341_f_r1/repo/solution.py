import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[idx]) - 1; v = int(data[idx + 1]) - 1
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    W = [int(data[idx + i]) for i in range(n)]
    idx += n
    A = [int(data[idx + i]) for i in range(n)]

    # f[x] = max number of operations started from a single piece on x.
    # f[x] = 1 + max sum of f[y] over S subset of N(x), sum W[y] <= W[x]-1.
    f = [0] * n
    order = sorted(range(n), key=lambda i: W[i])
    for x in order:
        cap = W[x] - 1
        dp = [0] * (cap + 1)
        for y in adj[x]:
            w = W[y]
            if w > cap:
                continue
            v = f[y]
            # 0/1 knapsack update: dp[c] = max(dp[c], dp[c-w] + v)
            shifted = [b + v for b in dp[:cap + 1 - w]]
            dp[w:] = list(map(max, dp[w:], shifted))
        f[x] = 1 + dp[cap] if cap >= 0 else 1

    ans = 0
    for i in range(n):
        ans += A[i] * f[i]
    print(ans)


main()
