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
    A = [int(data[idx + i]) - 1 for i in range(k)]
    idx += k
    B = [int(data[idx + i]) - 1 for i in range(k)]

    cntA = [0] * n
    cntB = [0] * n
    for x in A:
        cntA[x] += 1
    for x in B:
        cntB[x] += 1

    parent = list(range(n))
    size = [1] * n

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    total = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        a = cntA[ru] + cntA[rv]
        b = cntB[ru] + cntB[rv]
        mt = a if a < b else b
        total += mt * w
        cntA[ru] = a - mt
        cntB[ru] = b - mt
    print(total)


main()
