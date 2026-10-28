import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    H = [0] * (n + 2)
    for i in range(1, n + 1):
        H[i] = int(data[1 + i])
    # Next greater element and depth in NGE forest (sentinel n+1 = none)
    nge = [n + 1] * (n + 2)
    stack = []
    for i in range(n, 0, -1):
        h = H[i]
        while stack and H[stack[-1]] < h:
            stack.pop()
        nge[i] = stack[-1] if stack else n + 1
        stack.append(i)
    depth = [0] * (n + 2)
    for i in range(n, 0, -1):
        depth[i] = 1 + depth[nge[i]]
    # Sparse table for range max over H
    table = [H[1:n + 1]]
    k = 1
    while (1 << k) <= n:
        prev = table[-1]
        half = 1 << (k - 1)
        table.append(list(map(max, prev[:-half], prev[half:])))
        k += 1
    queries = []
    ptr = 2 + n
    for qi in range(q):
        l = int(data[ptr]); r = int(data[ptr + 1]); ptr += 2
        # max of H[l+1..r] (1-indexed) -> 0-indexed [l, r-1]
        a = l
        b = r - 1  # inclusive
        length = b - a + 1
        j = length.bit_length() - 1
        row = table[j]
        m = row[a] if row[a] > row[b - (1 << j) + 1] else row[b - (1 << j) + 1]
        queries.append((m, r, qi))
    queries.sort()
    # pos[v] = index with height v
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[H[i]] = i
    # DSU: find smallest active index >= x; active = height > current M
    parent = list(range(n + 2))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    ans = [0] * q
    cur = 0  # heights <= cur are deactivated
    for m, r, qi in queries:
        while cur < m:
            cur += 1
            p = pos[cur]
            parent[p] = p + 1
        p = find(r + 1)
        ans[qi] = depth[p] if p <= n else 0
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
