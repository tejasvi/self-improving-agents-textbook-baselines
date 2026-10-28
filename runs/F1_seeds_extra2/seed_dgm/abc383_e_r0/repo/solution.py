import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    cntA = [0] * n
    cntB = [0] * n
    for _ in range(k):
        cntA[int(data[idx]) - 1] += 1
        idx += 1
    for _ in range(k):
        cntB[int(data[idx]) - 1] += 1
        idx += 1

    parent = list(range(n))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    # Kruskal: f(x, y) is the weight of the edge that first connects x and y.
    # Greedily match leftover A's with leftover B's across each merge.
    edges.sort()
    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        a = cntA[ru] + cntA[rv]
        b = cntB[ru] + cntB[rv]
        t = a if a < b else b
        ans += w * t
        parent[ru] = rv
        cntA[rv] = a - t
        cntB[rv] = b - t
    print(ans)


main()
