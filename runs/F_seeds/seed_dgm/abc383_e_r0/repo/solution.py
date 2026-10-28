import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); m = int(data[pos + 1]); k = int(data[pos + 2])
    pos += 3
    edges = []
    for _ in range(m):
        u = int(data[pos]) - 1
        v = int(data[pos + 1]) - 1
        w = int(data[pos + 2])
        pos += 3
        edges.append((w, u, v))
    a = [0] * n
    b = [0] * n
    for _ in range(k):
        a[int(data[pos]) - 1] += 1
        pos += 1
    for _ in range(k):
        b[int(data[pos]) - 1] += 1
        pos += 1

    parent = list(range(n))

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
        m1 = min(a[ru], b[rv])
        m2 = min(a[rv], b[ru])
        ans += w * (m1 + m2)
        na = (a[ru] - m1) + (a[rv] - m2)
        nb = (b[ru] - m2) + (b[rv] - m1)
        parent[ru] = rv
        a[rv] = na
        b[rv] = nb
    print(ans)


main()
