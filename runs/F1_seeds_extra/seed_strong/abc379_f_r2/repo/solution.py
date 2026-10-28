import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    qs = []
    idx = 2 + n
    L = []; R = []
    for _ in range(q):
        L.append(int(data[idx])); R.append(int(data[idx + 1])); idx += 2

    # sparse table for range max over H[1..n]
    table = [H[:]]
    j = 1
    while (1 << j) <= n + 1:
        prev = table[-1]
        h = 1 << (j - 1)
        table.append(list(map(max, prev[:-h] if h else prev, prev[h:])))
        j += 1

    def rmq(a, b):  # max H[a..b], a<=b
        k = (b - a + 1).bit_length() - 1
        t = table[k]
        x = t[a]; y = t[b - (1 << k) + 1]
        return x if x > y else y

    # depth in next-greater-element tree; node n+1 is sentinel with depth 0
    nge = [n + 1] * (n + 2)
    depth = [0] * (n + 2)
    st = []
    for i in range(1, n + 1):
        h = H[i]
        while st and H[st[-1]] < h:
            nge[st.pop()] = i
        st.append(i)
    for i in range(n, 0, -1):
        depth[i] = depth[nge[i]] + 1

    M = [0] * q
    for t in range(q):
        M[t] = rmq(L[t] + 1, R[t])

    # DSU "next active" over positions 1..n+1; initially all active
    nxt = list(range(n + 3))

    def find(x):
        root = x
        while nxt[root] != root:
            root = nxt[root]
        while nxt[x] != root:
            nxt[x], x = root, nxt[x]
        return root

    order_pos = sorted(range(1, n + 1), key=lambda i: H[i])
    order_q = sorted(range(q), key=lambda t: M[t])
    ans = [0] * q
    ptr = 0
    for t in order_q:
        m = M[t]
        while ptr < n and H[order_pos[ptr]] <= m:
            p = order_pos[ptr]
            nxt[p] = p + 1
            ptr += 1
        p = find(R[t] + 1)
        ans[t] = depth[p] if p <= n else 0

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()
