import sys


def solve(n, s, t, K=26):
    f = [-1] * K
    for a, b in zip(s, t):
        x = ord(a) - 97
        y = ord(b) - 97
        if f[x] == -1:
            f[x] = y
        elif f[x] != y:
            return -1
    # Mapping is a function on present letters. Each present letter x with
    # f[x] != x is an edge. Compute components (undirected) via DSU.
    parent = list(range(K))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    touched = [False] * K
    edges = 0
    for x in range(K):
        if f[x] != -1 and f[x] != x:
            edges += 1
            touched[x] = True
            touched[f[x]] = True
            rx, ry = find(x), find(f[x])
            if rx != ry:
                parent[rx] = ry

    # A component is a pure cycle iff every node has in-degree exactly 1
    # within the component (then it is a single cycle with no trees).
    indeg = [0] * K
    for x in range(K):
        if f[x] != -1 and f[x] != x:
            indeg[f[x]] += 1
    nodes = {}
    bad = {}
    for x in range(K):
        if touched[x]:
            r = find(x)
            nodes[r] = nodes.get(r, 0) + 1
            if indeg[x] != 1:
                bad[r] = True
    cycles = 0
    cycle_letters = 0
    for r in nodes:
        if not bad.get(r, False):
            cycles += 1
            cycle_letters += nodes[r]

    if cycles > 0 and len(set(s)) == K:
        return -1
    return edges + cycles


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    t = data[2]
    print(solve(n, s, t))


if __name__ == "__main__":
    main()
