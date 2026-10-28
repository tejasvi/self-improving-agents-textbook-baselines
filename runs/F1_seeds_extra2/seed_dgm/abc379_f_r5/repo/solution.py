import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    idx = 2 + n

    # next greater element to the right (sentinel n+1)
    nxt = [n + 1] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            stack.pop()
        nxt[i] = stack[-1] if stack else n + 1
        stack.append(i)
    # depth in next-greater chain
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = 1 + depth[nxt[i]]

    # sparse table for range max over H[1..n]
    table = [H[1:n + 1]]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append(list(map(max, prev[:-half], prev[half:])))
        j += 1

    def rmq(lo, hi):  # 1-indexed inclusive
        length = hi - lo + 1
        k = length.bit_length() - 1
        t = table[k]
        a = t[lo - 1]
        b = t[hi - (1 << k)]
        return a if a > b else b

    ls = [0] * q
    rs = [0] * q
    Ms = [0] * q
    for t in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        ls[t] = l; rs[t] = r
        Ms[t] = rmq(l + 1, r)

    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[H[i]] = i

    parent = list(range(n + 3))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    order = sorted(range(q), key=Ms.__getitem__)
    ans = [0] * q
    removed = 0  # values 1..removed have been removed
    for t in order:
        M = Ms[t]
        while removed < M:
            removed += 1
            p = pos[removed]
            parent[p] = p + 1
        p = find(rs[t] + 1)
        ans[t] = 0 if p == n + 1 else depth[p]

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()
