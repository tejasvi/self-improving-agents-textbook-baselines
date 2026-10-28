import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    # pos[v] = index of value v (values are distinct)
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[H[i]] = i
    # next greater element (0 if none)
    ng = [0] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            stack.pop()
        ng[i] = stack[-1] if stack else 0
        stack.append(i)
    # depth[i] = number of nodes on next-greater chain starting at i
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = 1 + depth[ng[i]] if ng[i] else 1
    # sparse table over values, range max on H[l+1..r]
    sp = [H[1:n + 1]]
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
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # range [l+1, r] 1-indexed -> [l, r-1] 0-indexed in sp
        a = l; b = r - 1  # 0-indexed inclusive
        length = b - a + 1
        j = length.bit_length() - 1
        row = sp[j]
        m1 = row[a]; m2 = row[b - (1 << j) + 1]
        M = m1 if m1 > m2 else m2
        p = pos[M]
        g = ng[p]
        out.append(depth[g] if g else 0)
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
