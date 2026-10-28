import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    H = [0] * (n + 2)
    pos = [0] * (n + 2)
    for i in range(1, n + 1):
        h = int(data[1 + i])
        H[i] = h
        pos[h] = i

    # nxt[i]: nearest j > i with H[j] > H[i], or n+1 if none
    nxt = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nxt[stack.pop()] = i
        stack.append(i)

    # depth[i] = length of next-greater chain starting at i (depth[n+1] = 0)
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = 1 + depth[nxt[i]]

    # sparse table of max over H[1..n] (table[k][i] = max H[i+1 .. i+2^k])
    table = [H[1:n + 1]]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        table.append([max(a, b) for a, b in zip(prev, prev[half:])])
        j += 1

    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # M = max(H[l+1..r]) -> 0-based indices l .. r-1
        lo = l
        length = r - l
        k = length.bit_length() - 1
        t = table[k]
        a = t[lo]
        b = t[r - (1 << k)]
        mv = a if a > b else b
        f = nxt[pos[mv]]
        out.append(depth[f])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
