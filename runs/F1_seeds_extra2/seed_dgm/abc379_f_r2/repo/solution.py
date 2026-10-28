import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    h = [int(x) for x in data[2:2 + n]]

    # nge[i]: index of next greater element to the right (n if none)
    # depth[i]: length of next-greater chain starting at i
    nge = [n] * n
    stack = []
    for i in range(n):
        hi = h[i]
        while stack and h[stack[-1]] < hi:
            nge[stack.pop()] = i
        stack.append(i)
    depth = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        depth[i] = 1 + depth[nge[i]]

    # heights are a permutation of 1..N
    pos = [0] * (n + 1)
    for i, v in enumerate(h):
        pos[v] = i

    # sparse table for range max
    table = [h]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append(list(map(max, prev[:-half], prev[half:])))
        j += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        L = int(data[idx])
        R = int(data[idx + 1])
        idx += 2
        # buildings L+1..R (1-based) => 0-based indices L..R-1
        a = L
        b = R - 1
        k = (b - a + 1).bit_length() - 1
        row = table[k]
        v = max(row[a], row[b - (1 << k) + 1])
        m = pos[v]
        out.append(depth[nge[m]])

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
