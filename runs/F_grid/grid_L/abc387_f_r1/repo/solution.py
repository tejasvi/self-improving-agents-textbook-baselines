import sys
from collections import deque

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    A = [int(x) - 1 for x in data[2:2 + n]]

    indeg = [0] * n
    for v in range(n):
        indeg[A[v]] += 1

    # g[v][t] (t = 0..m-1 meaning value t+1): product over processed children c of prefix sums of f_c
    g = [None] * n
    ones = [1] * m
    for v in range(n):
        g[v] = ones[:]

    q = deque(v for v in range(n) if indeg[v] == 0)
    removed = [False] * n
    while q:
        v = q.popleft()
        removed[v] = True
        f = g[v]
        # prefix sums: S[t] = sum_{s<=t} f[s]
        S = [0] * m
        acc = 0
        for t in range(m):
            acc = (acc + f[t]) % MOD
            S[t] = acc
        p = A[v]
        g[p] = [a * b % MOD for a, b in zip(g[p], S)]
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    # remaining nodes lie on cycles
    visited = [False] * n
    ans = 1
    for s in range(n):
        if removed[s] or visited[s]:
            continue
        prod = [1] * m
        v = s
        while not visited[v]:
            visited[v] = True
            prod = [a * b % MOD for a, b in zip(prod, g[v])]
            v = A[v]
        ans = ans * (sum(prod) % MOD) % MOD

    print(ans % MOD)

main()
