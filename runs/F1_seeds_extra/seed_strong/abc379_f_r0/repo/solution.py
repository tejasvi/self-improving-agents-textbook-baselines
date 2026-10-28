import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [int(x) for x in data[2:2 + n]]
    # pos of value
    pos = [0] * (n + 1)
    for i, h in enumerate(H):
        pos[h] = i
    # next greater element (0-indexed), -1 if none
    nge = [-1] * n
    stack = []
    for i in range(n):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)
    # depth along nge chain: depth[i] = 1 + depth[nge[i]]
    depth = [0] * n
    for i in range(n - 1, -1, -1):
        j = nge[i]
        depth[i] = 1 if j < 0 else depth[j] + 1
    # sparse table of max values
    sp = [H]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        cur = [a if a > b else b for a, b in zip(prev, prev[half:])]
        sp.append(cur)
        k += 1
    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx])
        r = int(data[idx + 1]) - 1
        idx += 2
        length = r - l + 1
        lv = length.bit_length() - 1
        row = sp[lv]
        a = row[l]
        b = row[r - (1 << lv) + 1]
        M = a if a > b else b
        p = nge[pos[M]]
        out.append(depth[p] if p >= 0 else 0)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
