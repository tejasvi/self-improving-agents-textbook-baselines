import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [int(x) for x in data[2:2 + n]]

    # next greater element to the right (index n if none)
    nge = [n] * n
    stack = []
    for i in range(n):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)

    # depth[i] = number of chain nodes from i along nge (including i)
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = depth[nge[i]] + 1

    # sparse table for range max
    sp = [H]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        cur = list(map(max, prev[:n - (1 << k) + 1], prev[half:half + n - (1 << k) + 1]))
        sp.append(cur)
        k += 1
    LOG = len(sp) - 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx]) - 1; r = int(data[idx + 1]) - 1
        idx += 2
        a = l + 1; b = r
        ln = b - a + 1
        kk = ln.bit_length() - 1
        M = max(sp[kk][a], sp[kk][b - (1 << kk) + 1])
        # first index p > r with H[p] > M
        pos = r + 1
        for j in range(LOG, -1, -1):
            if pos + (1 << j) <= n and sp[j][pos] < M:
                pos += 1 << j
        out.append(depth[pos])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
