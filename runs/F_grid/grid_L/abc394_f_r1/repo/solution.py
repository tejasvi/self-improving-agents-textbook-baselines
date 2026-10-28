import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    if n < 4:
        print(-1)
        return
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    idx = 1
    for _ in range(n - 1):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        adj[a].append(b)
        adj[b].append(a)
        deg[a] += 1
        deg[b] += 1

    # BFS order from root 1
    parent = [0] * (n + 1)
    order = []
    visited = [False] * (n + 1)
    visited[1] = True
    stack = [1]
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if not visited[u]:
                visited[u] = True
                parent[u] = v
                stack.append(u)

    # dp[v]: max size of connected set K with top vertex v inside v's subtree,
    # where each vertex of K has degree <= 4 in K and deg_T >= 4.
    dp = [0] * (n + 1)
    best = 0
    for v in reversed(order):
        if deg[v] < 4:
            dp[v] = 0
            continue
        vals = []
        p = parent[v]
        for u in adj[v]:
            if u != p and dp[u] > 0:
                vals.append(dp[u])
        vals.sort(reverse=True)
        top3 = sum(vals[:3])
        top4 = top3 + (vals[3] if len(vals) > 3 else 0)
        dp[v] = 1 + top3
        cand = 1 + top4
        if cand > best:
            best = cand

    if best == 0:
        print(-1)
    else:
        print(3 * best + 2)


main()
