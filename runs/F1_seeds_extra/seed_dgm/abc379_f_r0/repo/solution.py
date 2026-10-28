import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    h = [0] * (n + 2)  # 1-indexed heights
    for i in range(n):
        h[i + 1] = int(data[2 + i])
    pos = [0] * (n + 1)  # height value -> index
    for i in range(1, n + 1):
        pos[h[i]] = i

    # nge[i]: next index j>i with h[j]>h[i], or n+1 if none
    nge = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        hi = h[i]
        while stack and h[stack[-1]] < hi:
            nge[stack.pop()] = i
        stack.append(i)

    # depth[i] = number of nodes in chain i -> nge -> ... (within 1..n)
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = 1 + depth[nge[i]]

    # sparse table of max over h[1..n]
    table = [h[1:n + 1]]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        cur = [a if a > b else b for a, b in zip(prev, prev[half:])]
        table.append(cur)
        k += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        # max over h[l+1..r] (1-indexed) -> table indices l..r-1 (0-indexed)
        lo = l
        hi_ = r - 1  # inclusive 0-indexed
        length = hi_ - lo + 1
        j = length.bit_length() - 1
        t = table[j]
        a = t[lo]
        b = t[hi_ - (1 << j) + 1]
        mv = a if a > b else b
        m = pos[mv]
        out.append(depth[nge[m]])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
