import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    p = 3
    edges = []
    for _ in range(m):
        u = int(data[p]); v = int(data[p + 1]); w = int(data[p + 2])
        p += 3
        edges.append((w, u, v))
    A = data[p:p + k]; p += k
    B = data[p:p + k]; p += k
    ca = [0] * (n + 1)
    cb = [0] * (n + 1)
    for x in A:
        ca[int(x)] += 1
    for x in B:
        cb[int(x)] += 1
    parent = list(range(n + 1))

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
        a = ca[ru] + ca[rv]
        b = cb[ru] + cb[rv]
        mt = a if a < b else b
        total += mt * w
        parent[rv] = ru
        ca[ru] = a - mt
        cb[ru] = b - mt
    print(total)

main()
