import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[H[i]] = i

    # next greater element (index), 0 if none
    nge = [0] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            stack.pop()
        nge[i] = stack[-1] if stack else 0
        stack.append(i)

    # depth in nge forest
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        g = nge[i]
        depth[i] = depth[g] + 1 if g else 0

    # sparse table of max values
    sp = [H[1:n + 1]]
    j = 1
    while (1 << j) <= n:
        prev = sp[-1]
        half = 1 << (j - 1)
        cur = [a if a > b else b for a, b in zip(prev, prev[half:])]
        sp.append(cur)
        j += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        # range [l+1, r] in 1-based -> [l, r-1] in 0-based sp
        lo = l
        hi = r - 1  # inclusive, 0-based
        k = (hi - lo + 1).bit_length() - 1
        row = sp[k]
        a = row[lo]
        b = row[hi - (1 << k) + 1]
        mv = a if a > b else b
        m = pos[mv]
        out.append(depth[m])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
