import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    h = [0] * (n + 2)
    for i in range(n):
        h[i + 1] = int(data[2 + i])
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[h[i]] = i

    # next greater element index (0 if none), 1-indexed
    nge = [0] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        hi = h[i]
        while stack and h[stack[-1]] < hi:
            nge[stack.pop()] = i
        stack.append(i)

    # depth in next-greater forest: depth[i] = 0 if nge none, else depth[nge]+1
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        g = nge[i]
        depth[i] = depth[g] + 1 if g else 0

    # sparse table of max values over h[1..n]
    table = [h[1:n + 1]]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        cur = list(map(max, prev[:len(prev) - half], prev[half:]))
        table.append(cur)
        j += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        # range [l+1, r] in 1-indexed -> [l, r-1] 0-indexed in table
        a = l
        b = r - 1
        length = b - a + 1
        k = length.bit_length() - 1
        t = table[k]
        m1 = t[a]
        m2 = t[b - (1 << k) + 1]
        m = m1 if m1 > m2 else m2
        p = pos[m]
        out.append(depth[p])

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
