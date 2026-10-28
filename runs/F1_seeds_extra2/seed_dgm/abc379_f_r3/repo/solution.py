import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [int(x) for x in data[2:2 + n]]
    qs = data[2 + n:2 + n + 2 * q]

    # next greater element index (N if none); depth = number of records in chain
    ng = [n] * n
    stack = []
    for i in range(n):
        h = H[i]
        while stack and H[stack[-1]] < h:
            ng[stack.pop()] = i
        stack.append(i)
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = 1 + depth[ng[i]]

    # sparse table for range max
    sp = [H]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        sp.append(list(map(max, prev[:-half] if half else prev, prev[half:])))
        k += 1

    def rmax(a, b):  # inclusive, a<=b
        length = b - a + 1
        j = length.bit_length() - 1
        t = sp[j]
        x = t[a]; y = t[b - (1 << j) + 1]
        return x if x > y else y

    Ms = [0] * q
    Rs = [0] * q
    for i in range(q):
        l = int(qs[2 * i]) - 1
        r = int(qs[2 * i + 1]) - 1
        Ms[i] = rmax(l + 1, r)
        Rs[i] = r + 1  # start index for successor search

    # DSU "next alive index": index deleted when its height <= M
    parent = list(range(n + 2))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    pos = [0] * (n + 1)
    for i, h in enumerate(H):
        pos[h] = i

    order = sorted(range(q), key=Ms.__getitem__)
    ans = [0] * q
    v = 1  # next height value to delete
    for qi in order:
        M = Ms[qi]
        while v <= M:
            idx = pos[v]
            parent[idx] = idx + 1
            v += 1
        p = find(Rs[qi])
        if p >= n:
            ans[qi] = 0
        else:
            ans[qi] = depth[p]

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()
