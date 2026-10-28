import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    qs = data[2 + n:]

    # next greater element and depth in the next-greater tree (root = n+1)
    nge = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)
    depth = [0] * (n + 2)
    for j in range(n, 0, -1):
        depth[j] = depth[nge[j]] + 1

    # sparse table for range max over H[1..n]
    sp = [H[:]]
    k = 1
    while (1 << k) <= n + 1:
        prev = sp[-1]
        half = 1 << (k - 1)
        cur = [max(a, b) for a, b in zip(prev, prev[half:])]
        sp.append(cur)
        k += 1

    L = [0] * q
    R = [0] * q
    M = [0] * q
    for t in range(q):
        l = int(qs[2 * t])
        r = int(qs[2 * t + 1])
        L[t] = l
        R[t] = r
        a = l + 1
        length = r - l
        kk = length.bit_length() - 1
        row = sp[kk]
        x = row[a]
        y = row[r - (1 << kk) + 1]
        M[t] = x if x > y else y

    # offline: process queries by M ascending, removing positions with H <= M
    # DSU "next active position" structure
    parent = list(range(n + 3))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pos_sorted = sorted(range(1, n + 1), key=lambda i: H[i])
    order = sorted(range(q), key=lambda t: M[t])
    ans = [0] * q
    p = 0
    for t in order:
        m = M[t]
        while p < n and H[pos_sorted[p]] <= m:
            idx = pos_sorted[p]
            parent[idx] = idx + 1
            p += 1
        j = find(R[t] + 1)
        ans[t] = depth[j] if j <= n else 0

    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
