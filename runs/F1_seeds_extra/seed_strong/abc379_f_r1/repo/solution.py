import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    H = [0] + [int(x) for x in data[2:2 + n]] + [0]
    # sparse table for range max; sp[j][i] = max(H[i .. i+2^j-1])
    sp = [H]
    j = 1
    while (1 << j) <= n:
        prev = sp[-1]
        h = 1 << (j - 1)
        sp.append([a if a > b else b for a, b in zip(prev, prev[h:])])
        j += 1
    # depth in next-greater-element forest; depth[n+1] = 0
    depth = [0] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        hi = H[i]
        while stack and H[stack[-1]] < hi:
            stack.pop()
        nxt = stack[-1] if stack else n + 1
        depth[i] = depth[nxt] + 1
        stack.append(i)
    out = []
    idx = 2 + n
    levels = list(range(len(sp)))[::-1]
    for _ in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # M = max H[l+1..r]
        L = l + 1
        k = (r - L + 1).bit_length() - 1
        a = sp[k][L]; b = sp[k][r - (1 << k) + 1]
        M = a if a > b else b
        # first position p > r with H[p] > M (n+1 if none)
        pos = r + 1
        for jj in levels:
            if pos + (1 << jj) - 1 <= n and sp[jj][pos] <= M:
                pos += 1 << jj
        out.append(depth[pos])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
