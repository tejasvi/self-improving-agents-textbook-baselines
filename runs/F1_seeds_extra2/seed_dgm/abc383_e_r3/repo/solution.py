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
    a = [0] * n  # leftover A-count per DSU root
    b = [0] * n  # leftover B-count per DSU root
    for i in range(k):
        a[int(data[idx + i]) - 1] += 1
    idx += k
    for i in range(k):
        b[int(data[idx + i]) - 1] += 1

    parent = list(range(n))

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
        na = a[ru] + a[rv]
        nb = b[ru] + b[rv]
        mt = na if na < nb else nb
        total += w * mt
        parent[ru] = rv
        a[rv] = na - mt
        b[rv] = nb - mt
    print(total)


main()
