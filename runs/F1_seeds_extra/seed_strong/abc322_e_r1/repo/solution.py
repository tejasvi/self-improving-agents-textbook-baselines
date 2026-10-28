import sys

def main():
    data = sys.stdin.read().split()
    n, k, p = int(data[0]), int(data[1]), int(data[2])
    idx = 3
    base = p + 1
    S = base ** k
    INF = float('inf')
    dp = [INF] * S
    dp[0] = 0
    for _ in range(n):
        c = int(data[idx]); idx += 1
        a = [int(x) for x in data[idx:idx + k]]
        idx += k
        # T[s] = target state after applying plan to state s (capped at p)
        T = [0]
        mul = 1
        for j in range(k):
            f = [min(d + a[j], p) * mul for d in range(base)]
            T = [x + fd for fd in f for x in T]
            mul *= base
        ndp = dp[:]
        for s in range(S):
            v = dp[s]
            if v != INF:
                t = T[s]
                nv = v + c
                if nv < ndp[t]:
                    ndp[t] = nv
        dp = ndp
    ans = dp[S - 1]
    print(-1 if ans == INF else ans)

main()
