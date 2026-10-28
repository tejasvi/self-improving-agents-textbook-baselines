import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx+1]); k = int(data[idx+2]); idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx+1]); w = int(data[idx+2]); idx += 3
        edges.append((w, u, v))
    net = [0] * (n + 1)
    for i in range(k):
        net[int(data[idx + i])] += 1
    idx += k
    for i in range(k):
        net[int(data[idx + i])] -= 1
    edges.sort()
    parent = list(range(n + 1))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    total = 0
    for w, u, v in edges:
        ru = find(u); rv = find(v)
        if ru == rv:
            continue
        a = net[ru]; b = net[rv]
        if a * b < 0:
            total += w * min(abs(a), abs(b))
        parent[rv] = ru
        net[ru] = a + b
    print(total)

main()
