import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    # next greater element (strictly greater; heights are distinct)
    NGE = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            NGE[stack.pop()] = i
        stack.append(i)
    # depth[i] = number of hops along NGE chain from i to virtual root n+1
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = depth[NGE[i]] + 1
    # ans indexed by height value: for position p, answer = depth[NGE[p]]
    ansv = [0] * (n + 2)
    for p in range(1, n + 1):
        ansv[H[p]] = depth[NGE[p]]
    # sparse table of max values over positions 1..n
    table = [H[1:n + 1]]
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
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # range (l, r] in 1-based -> 0-based [l, r-1]
        lo = l
        hi = r - 1  # inclusive, 0-based
        length = hi - lo + 1
        j = length.bit_length() - 1
        row = table[j]
        a = row[lo]
        b = row[hi - (1 << j) + 1]
        m = a if a > b else b
        out.append(ansv[m])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
