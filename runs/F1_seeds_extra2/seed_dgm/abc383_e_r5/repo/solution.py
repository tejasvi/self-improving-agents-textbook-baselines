import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2])
    idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = [int(x) - 1 for x in data[idx:idx + k]]
    idx += k
    B = [int(x) - 1 for x in data[idx:idx + k]]

    parent = list(range(n))
    cntA = [0] * n
    cntB = [0] * n
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            nxt = parent[x]
            parent[x] = root
            x = nxt
        return root

    # Kruskal-style: at each merge with weight w, match as many A/B pairs
    # as possible inside the merged component (their bottleneck is w).
    edges.sort()
    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        a = cntA[ru] + cntA[rv]
        b = cntB[ru] + cntB[rv]
        mm = min(a, b)
        ans += mm * w
        parent[ru] = rv
        cntA[rv] = a - mm
        cntB[rv] = b - mm
    print(ans)


main()
