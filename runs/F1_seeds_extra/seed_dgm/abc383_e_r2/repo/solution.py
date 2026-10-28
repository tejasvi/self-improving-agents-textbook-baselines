import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = [int(x) for x in data[idx:idx + k]]
    idx += k
    B = [int(x) for x in data[idx:idx + k]]

    # signed count per vertex: + for A occurrences, - for B occurrences
    val = [0] * (n + 1)
    for a in A:
        val[a] += 1
    for b in B:
        val[b] -= 1

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
        x = val[ru]
        y = val[rv]
        if (x > 0 and y < 0) or (x < 0 and y > 0):
            total += w * min(abs(x), abs(y))
        parent[rv] = ru
        val[ru] = x + y
    print(total)


main()
