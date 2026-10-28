import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    edges = []
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
        edges.append((u, v))

    # DSU over degree-3 vertices, joined by tree edges between them
    parent = list(range(n + 1))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    for u, v in edges:
        if deg[u] == 3 and deg[v] == 3:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv

    # For each degree-2 vertex, each degree-3 neighbor gives an attachment
    cnt = [0] * (n + 1)
    for u in range(1, n + 1):
        if deg[u] == 2:
            for x in adj[u]:
                if deg[x] == 3:
                    cnt[find(x)] += 1

    ans = 0
    for k in cnt:
        if k >= 2:
            ans += k * (k - 1) // 2
    print(ans)


main()
