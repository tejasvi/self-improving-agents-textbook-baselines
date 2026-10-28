import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [int(x) for x in data[2:2 + n]]

    # nge[i]: index of next greater element to the right (n if none)
    nge = [n] * n
    stack = []
    for i in range(n):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)

    # depth[i]: length of next-greater chain starting at i (including i)
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = depth[nge[i]] + 1

    # sparse table of argmax indices over H (0-indexed)
    sp = [list(range(n))]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        cur = []
        for i in range(n - (1 << k) + 1):
            x = prev[i]
            y = prev[i + half]
            cur.append(x if H[x] > H[y] else y)
        sp.append(cur)
        k += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx]) - 1
        r = int(data[idx + 1]) - 1
        idx += 2
        # argmax over 0-indexed positions [l+1, r]
        a = l + 1
        length = r - a + 1
        j = length.bit_length() - 1
        x = sp[j][a]
        y = sp[j][r - (1 << j) + 1]
        m = x if H[x] > H[y] else y
        g = nge[m]
        out.append(depth[g] if g < n else 0)

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
