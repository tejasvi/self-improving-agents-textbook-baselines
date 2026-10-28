import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2])
    idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]) - 1; v = int(data[idx + 1]) - 1; w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    cA = [0] * n
    cB = [0] * n
    for i in range(k):
        cA[int(data[idx + i]) - 1] += 1
    idx += k
    for i in range(k):
        cB[int(data[idx + i]) - 1] += 1
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
        x = find(u)
        y = find(v)
        if x == y:
            continue
        # match leftover A of one side with leftover B of the other side at cost w
        m1 = min(cA[x], cB[y])
        m2 = min(cA[y], cB[x])
        if m1 or m2:
            total += w * (m1 + m2)
        na = cA[x] + cA[y] - m1 - m2
        nb = cB[x] + cB[y] - m1 - m2
        parent[y] = x
        cA[x] = na
        cB[x] = nb
    print(total)


main()
