# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    sys.setrecursionlimit(1_000_000)
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [0] + [int(next(it)) for _ in range(n)]  # 1-indexed

    # leftDistinct[i]: number of distinct in A[1..i]
    leftDistinct = [0] * (n + 1)
    seen = set()
    cnt = 0
    for i in range(1, n + 1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        leftDistinct[i] = cnt

    # rightDistinct[i]: number of distinct in A[i..n]
    rightDistinct = [0] * (n + 2)
    seen.clear()
    cnt = 0
    for i in range(n, 0, -1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        rightDistinct[i] = cnt

    # next occurrence for each position
    nextPos = [n + 1] * (n + 1)
    next_occ = {}
    for i in range(n, 0, -1):
        val = A[i]
        if val in next_occ:
            nextPos[i] = next_occ[val]
        else:
            nextPos[i] = n + 1
        next_occ[val] = i

    # Segment tree for range add and range max over positions 1..n-1
    size = 1
    while size < n:
        size <<= 1
    INF_NEG = -10**9
    seg = [INF_NEG] * (2 * size)
    lazy = [0] * (2 * size)

    # Initialize leaves with rightDistinct[j+1]
    for j in range(1, n):  # j from 1 to n-1
        seg[size + j - 1] = rightDistinct[j + 1]
    for i in range(size - 1, 0, -1):
        seg[i] = max(seg[2 * i], seg[2 * i + 1])

    def apply(node, val):
        seg[node] += val
        lazy[node] += val

    def push(node):
        if lazy[node]:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = 0

    def range_add(l, r, val, node, node_l, node_r):
        if l > node_r or r < node_l:
            return
        if l <= node_l and node_r <= r:
            apply(node, val)
            return
        push(node)
        mid = (node_l + node_r) // 2
        range_add(l, r, val, node * 2, node_l, mid)
        range_add(l, r, val, node * 2 + 1, mid + 1, node_r)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def query_max(l, r, node, node_l, node_r):
        if l > node_r or r < node_l:
            return INF_NEG
        if l <= node_l and node_r <= r:
            return seg[node]
        push(node)
        mid = (node_l + node_r) // 2
        return max(query_max(l, r, node * 2, node_l, mid),
                   query_max(l, r, node * 2 + 1, mid + 1, node_r))

    best_from = [0] * (n + 2)  # best_from[s] for s in [1, n]
    # Process s from n-1 down to 1
    for s in range(n - 1, 0, -1):
        nxt = nextPos[s]
        l = s
        r = min(nxt - 1, n - 1)
        if l <= r:
            range_add(l, r, 1, 1, 1, size)
        best_from[s] = query_max(s, n - 1, 1, 1, size)

    ans = 0
    for i in range(1, n - 1):
        ans = max(ans, leftDistinct[i] + best_from[i + 1])
    print(ans)

if __name__ == "__main__":
    solve()
