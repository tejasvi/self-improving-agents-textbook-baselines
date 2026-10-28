import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    pos = [0] * (n + 2)
    for i in range(1, n + 1):
        h = int(data[1 + i])
        H[i] = h
        pos[h] = i
    # next greater element (index), n+1 if none
    nge = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)
    # depth in nge forest: depth[i] = 1 + depth[nge[i]], depth[n+1] = 0
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = depth[nge[i]] + 1
    # sparse table of max values over H[1..n]
    table = [H[1:n + 1]]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append([a if a > b else b for a, b in zip(prev, prev[half:])])
        j += 1
    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # max over H[l..r] -> positions l..r, table index l-1 .. r-1
        length = r - l + 1
        k = length.bit_length() - 1
        t = table[k]
        a = t[l - 1]
        b = t[r - (1 << k)]
        v = a if a > b else b
        m = pos[v]
        out.append(depth[nge[m]])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
