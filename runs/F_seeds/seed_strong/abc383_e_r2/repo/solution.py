import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2])
    idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = [int(x) for x in data[idx:idx + k]]
    idx += k
    B = [int(x) for x in data[idx:idx + k]]

    parent = list(range(n + 1))
    ca = [0] * (n + 1)
    cb = [0] * (n + 1)
    for x in A:
        ca[x] += 1
    for x in B:
        cb[x] += 1

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    ans = 0
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        a = ca[ru] + ca[rv]
        b = cb[ru] + cb[rv]
        mt = a if a < b else b
        if mt:
            ans += w * mt
            a -= mt
            b -= mt
        parent[rv] = ru
        ca[ru] = a
        cb[ru] = b
    print(ans)


main()
