import sys
from collections import deque

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    a = [int(x) - 1 for x in data[2:2 + n]]

    indeg = [0] * n
    for i in range(n):
        indeg[a[i]] += 1

    # g[u][v] = product over already-processed children c of S_c(v), v = 0..m-1
    g = [[1] * m for _ in range(n)]
    removed = [False] * n
    q = deque(i for i in range(n) if indeg[i] == 0)

    while q:
        u = q.popleft()
        removed[u] = True
        # S_u(v) = sum_{w<=v} f_u(w), where f_u = g[u]
        s = [0] * m
        acc = 0
        gu = g[u]
        for v in range(m):
            acc = (acc + gu[v]) % MOD
            s[v] = acc
        p = a[u]
        gp = g[p]
        for v in range(m):
            gp[v] = gp[v] * s[v] % MOD
        indeg[p] -= 1
        if indeg[p] == 0:
            q.append(p)

    ans = 1
    visited = [False] * n
    for i in range(n):
        if removed[i] or visited[i]:
            continue
        # traverse the cycle containing i
        prod = [1] * m
        u = i
        while not visited[u]:
            visited[u] = True
            gu = g[u]
            for v in range(m):
                prod[v] = prod[v] * gu[v] % MOD
            u = a[u]
        ans = ans * (sum(prod) % MOD) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    main()
