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
    # net[x] = (#A unmatched) - (#B unmatched) in component of x
    net = [0] * (n + 1)
    for i in range(k):
        net[int(data[p + i])] += 1
    p += k
    for i in range(k):
        net[int(data[p + i])] -= 1
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
        a = find(u)
        b = find(v)
        if a == b:
            continue
        na = net[a]
        nb = net[b]
        if (na > 0 and nb < 0) or (na < 0 and nb > 0):
            total += w * min(abs(na), abs(nb))
        parent[a] = b
        net[b] = na + nb
    print(total)


main()
