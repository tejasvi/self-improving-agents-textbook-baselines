# Write your solution here. Read from stdin, write to stdout.
import sys

def main():
    sys.setrecursionlimit(1_000_000)
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n)]
    deg = [0] * n
    edges = []
    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1
        edges.append((u, v))
    # leaf status
    is_leaf = [d == 1 for d in deg]
    # leaf_adj_count[v] = number of leaf neighbors of v
    leaf_adj = [0] * n
    for u, v in edges:
        if is_leaf[u]:
            leaf_adj[v] += 1
        if is_leaf[v]:
            leaf_adj[u] += 1
    max_keep = 0
    # consider each vertex as the central vertex of the snowflake
    for c in range(n):
        caps = []  # capacities (available leaf children) for each neighbor of c
        for nb in adj[c]:
            # capacity is leaf_adj[nb] minus 1 if c itself is a leaf neighbor of nb
            cap = leaf_adj[nb]
            if is_leaf[c]:
                # c is a leaf, therefore it was counted in leaf_adj[nb]
                cap -= 1
            if cap > 0:
                caps.append(cap)
        if not caps:
            continue
        caps.sort(reverse=True)
        # iterate over possible number of branch nodes (x) as prefix length
        for i, y in enumerate(caps, start=1):
            # y is the capacity of the i-th selected branch node (the smallest among selected)
            if y <= 0:
                break
            keep = 1 + i + i * y  # center + x branches + x*y leaves
            if keep > max_keep:
                max_keep = keep
    # answer is vertices to delete
    print(n - max_keep)

if __name__ == "__main__":
    main()
