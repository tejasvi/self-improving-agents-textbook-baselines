import sys
from collections import deque


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    names = data[1:1 + n]
    V = 26
    idx = lambda c: ord(c) - 65

    # reflexive reachability on the 26 letters
    reach = [[False] * V for _ in range(V)]
    for i in range(V):
        reach[i][i] = True
    edges = []
    for s in names:
        u, v = idx(s[0]), idx(s[1])
        edges.append((u, v))
        reach[u][v] = True
    for k in range(V):
        rk = reach[k]
        for i in range(V):
            if reach[i][k]:
                ri = reach[i]
                for j in range(V):
                    if rk[j]:
                        ri[j] = True

    def same_scc(a, b):
        return reach[a][b] and reach[b][a]

    # Build items: (tail, head) vertices; big SCC items use a representative vertex
    # for both tail and head.
    items = []
    scc_rep_done = {}  # representative vertex -> item created
    for u, v in edges:
        if same_scc(u, v):
            # internal edge of a strongly connected component (possibly self-loop)
            rep = min(w for w in range(V) if same_scc(u, w))
            if rep not in scc_rep_done:
                scc_rep_done[rep] = len(items)
                items.append((rep, rep))
        else:
            items.append((u, v))
    m = len(items)
    if m == 0:
        print(0)
        return

    # adjacency: x -> y if head(x) reaches tail(y), x != y
    adj = [[] for _ in range(m)]
    for x in range(m):
        hx = items[x][1]
        rh = reach[hx]
        for y in range(m):
            if x != y and rh[items[y][0]]:
                adj[x].append(y)

    # Hopcroft-Karp maximum bipartite matching
    INF = float('inf')
    match_l = [-1] * m
    match_r = [-1] * m
    dist = [0] * m

    def bfs():
        q = deque()
        found = False
        for u in range(m):
            if match_l[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        while q:
            u = q.popleft()
            for w in adj[u]:
                p = match_r[w]
                if p == -1:
                    found = True
                elif dist[p] == INF:
                    dist[p] = dist[u] + 1
                    q.append(p)
        return found

    def dfs(root):
        # iterative DFS for augmenting path
        stack = [(root, 0)]
        path = []
        while stack:
            u, i = stack[-1]
            advanced = False
            while i < len(adj[u]):
                w = adj[u][i]
                i += 1
                p = match_r[w]
                if p == -1:
                    # augment along stack
                    stack[-1] = (u, i)
                    path.append(w)
                    for k in range(len(stack)):
                        uu = stack[k][0]
                        ww = path[k]
                        match_l[uu] = ww
                        match_r[ww] = uu
                    return True
                if dist[p] == dist[u] + 1:
                    stack[-1] = (u, i)
                    path.append(w)
                    stack.append((p, 0))
                    advanced = True
                    break
            if not advanced:
                dist[u] = INF
                stack.pop()
                if path:
                    path.pop()
        return False

    matching = 0
    while bfs():
        for u in range(m):
            if match_l[u] == -1 and dfs(u):
                matching += 1

    print(m - matching)


main()
