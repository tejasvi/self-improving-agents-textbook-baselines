import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); q = int(data[1])
    H = [0] * (n + 2)
    for i in range(n):
        H[i + 1] = int(data[2 + i])
    # next greater element (sentinel n+1 if none)
    nge = [n + 1] * (n + 2)
    stack = []
    for i in range(1, n + 1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            nge[stack.pop()] = i
        stack.append(i)
    # depth[i] = number of nodes on chain i -> nge -> ... (depth[n+1] = 0)
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = depth[nge[i]] + 1
    depth[n + 1] = 0
    # position of each value
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[H[i]] = i
    # sparse table of range max over values (1-indexed array H[1..n])
    base = H[1:n + 1]
    sp = [base]
    k = 1
    while (1 << k) <= n:
        prev = sp[-1]
        half = 1 << (k - 1)
        sp.append(list(map(max, prev[:-half], prev[half:])))
        k += 1
    out = []
    idx = 2 + n
    for _ in range(q):
        l = int(data[idx]); r = int(data[idx + 1]); idx += 2
        # max over H[l+1..r], 1-indexed -> base indices l..r-1
        length = r - l
        j = length.bit_length() - 1
        row = sp[j]
        mx = max(row[l], row[r - (1 << j)])
        m = pos[mx]
        out.append(depth[nge[m]])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()
