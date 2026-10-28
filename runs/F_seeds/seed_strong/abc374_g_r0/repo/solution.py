import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    INF = 10 ** 9
    V = 28
    SRC, SNK = 26, 27
    cap = [[0] * V for _ in range(V)]
    e = [0] * 26
    used = [False] * 26
    parent = list(range(26))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s in names:
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        cap[u][v] = INF
        e[u] += 1
        e[v] -= 1
        used[u] = used[v] = True
        parent[find(u)] = find(v)

    for v in range(26):
        if e[v] < 0:
            cap[SRC][v] = -e[v]
        elif e[v] > 0:
            cap[v][SNK] = e[v]
    orig_src = cap[SRC][:]

    # Edmonds-Karp
    while True:
        par = [-1] * V
        par[SRC] = SRC
        q = deque([SRC])
        while q and par[SNK] == -1:
            x = q.popleft()
            row = cap[x]
            for y in range(V):
                if row[y] > 0 and par[y] == -1:
                    par[y] = x
                    q.append(y)
        if par[SNK] == -1:
            break
        f = INF
        y = SNK
        while y != SRC:
            x = par[y]
            f = min(f, cap[x][y])
            y = x
        y = SNK
        while y != SRC:
            x = par[y]
            cap[x][y] -= f
            cap[y][x] += f
            y = x

    # per component accounting
    surplus = {}
    flow = {}
    for v in range(26):
        if not used[v]:
            continue
        r = find(v)
        surplus.setdefault(r, 0)
        flow.setdefault(r, 0)
        if e[v] > 0:
            surplus[r] += e[v]
        elif e[v] < 0:
            flow[r] += orig_src[v] - cap[SRC][v]

    ans = 0
    for r in surplus:
        ans += max(1, surplus[r] - flow[r])
    print(ans)

main()
