import sys
from collections import Counter


def solve(N, S, T):
    # Each letter of S must map to exactly one letter of T.
    mapping = {}
    for s, t in zip(S, T):
        if s in mapping and mapping[s] != t:
            return -1
        mapping[s] = t
    edges = {s: t for s, t in mapping.items() if s != t}
    if not edges:
        return 0

    # Union-find over letters involved in the mapping edges.
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for s, t in edges.items():
        a, b = find(s), find(t)
        if a != b:
            parent[a] = b

    comp_nodes = {}
    for l in set(edges) | set(edges.values()):
        comp_nodes.setdefault(find(l), []).append(l)
    comp_edges = Counter(find(s) for s in edges)
    indeg = Counter(edges.values())

    # A temporary letter is available if some letter is absent from S,
    # or some component is a tree (its operations free a letter).
    has_tree = any(comp_edges[r] != len(ls) for r, ls in comp_nodes.items())
    free = len(set(S)) < 26 or has_tree

    ans = 0
    for r, ls in comp_nodes.items():
        k = len(ls)
        if comp_edges[r] == k:  # contains a cycle
            pure = all(l in edges and indeg[l] == 1 for l in ls)
            if pure:
                if not free:
                    return -1
                ans += k + 1
            else:
                ans += k
        else:
            ans += k - 1
    return ans


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1]
    T = data[2]
    print(solve(N, S, T))


if __name__ == "__main__":
    main()
