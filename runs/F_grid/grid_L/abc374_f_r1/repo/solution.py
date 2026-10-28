import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n, k, x = int(data[0]), int(data[1]), int(data[2])
    t = [int(v) for v in data[3:3 + n]]
    t.sort()
    # prefix sums of T (1-indexed orders)
    P = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + t[i]

    # candidate shipment days: T_r + m*X, m in [0, n)
    cand = sorted(set(t[r] + m * x for r in range(n) for m in range(n)))
    M = len(cand)
    INF = float('inf')

    # pm[i]: min over processed candidates c (C[c] <= C[d]-X) of g[c][i]
    pm = [INF] * (n + 1)
    pm[0] = 0  # no previous shipment: start state
    g_all = [None] * M
    ptr = 0
    best_answer = INF

    for d in range(M):
        C = cand[d]
        while ptr < M and cand[ptr] <= C - x:
            gp = g_all[ptr]
            if gp is not None:
                for i in range(n + 1):
                    if gp[i] < pm[i]:
                        pm[i] = gp[i]
            ptr += 1
        # h[i] = pm[i] + P[i] - i*C
        h = [INF] * (n + 1)
        for i in range(n + 1):
            if pm[i] != INF:
                h[i] = pm[i] + P[i] - i * C
        g = [INF] * (n + 1)
        dq = deque()  # indices i with increasing h
        # for i' from 1..n, window i in [i'-k, i'-1]
        nxt = 0  # next index to push
        for ip in range(1, n + 1):
            # push indices up to ip-1
            while nxt <= ip - 1:
                hv = h[nxt]
                while dq and h[dq[-1]] >= hv:
                    dq.pop()
                dq.append(nxt)
                nxt += 1
            while dq and dq[0] < ip - k:
                dq.popleft()
            if not dq or t[ip - 1] > C:
                continue
            mn = h[dq[0]]
            if mn == INF:
                continue
            g[ip] = ip * C - P[ip] + mn
        g_all[d] = g
        if g[n] < best_answer:
            best_answer = g[n]

    print(int(best_answer))


main()
