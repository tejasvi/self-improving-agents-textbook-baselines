import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    H = [int(x) for x in data[2:2 + n]]

    # depth[i] = length of the "next greater" chain starting at i (including i).
    nxt = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        hi = H[i]
        while stack and H[stack[-1]] < hi:
            stack.pop()
        nxt[i] = stack[-1] if stack else n
        stack.append(i)
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = depth[nxt[i]] + 1

    # sparse table for range max: table[k][i] = max H[i .. i+2^k-1]
    table = [H]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        h = 1 << (k - 1)
        table.append(list(map(max, prev[:len(prev) - h], prev[h:])))
        k += 1
    LOG = len(table)

    lg = [0] * (n + 2)
    for i in range(2, n + 2):
        lg[i] = lg[i >> 1] + 1

    out = []
    p = 2 + n
    for _ in range(q):
        l0 = int(data[p]) - 1
        r0 = int(data[p + 1]) - 1
        p += 2
        # M = max H[l0+1 .. r0]
        a = l0 + 1
        kk = lg[r0 - a + 1]
        t = table[kk]
        M = max(t[a], t[r0 - (1 << kk) + 1])
        # first position pos >= r0+1 with H[pos] > M (n if none)
        pos = r0 + 1
        for j in range(LOG - 1, -1, -1):
            if pos + (1 << j) <= n and table[j][pos] <= M:
                pos += 1 << j
        out.append(depth[pos])

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()
