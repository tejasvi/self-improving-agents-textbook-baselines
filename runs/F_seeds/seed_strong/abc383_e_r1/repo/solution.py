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
    B = data[p:p + k]
    sur = [0] * (n + 1)
    for x in A:
        sur[int(x)] += 1
    for x in B:
        sur[int(x)] -= 1
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
        ru = find(u); rv = find(v)
        if ru == rv:
            continue
        su = sur[ru]; sv = sur[rv]
        if (su > 0 and sv < 0) or (su < 0 and sv > 0):
            total += w * min(abs(su), abs(sv))
        parent[ru] = rv
        sur[rv] = su + sv
    print(total)

main()
