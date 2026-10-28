# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]

    # prefix distinct counts
    pref = [0] * n
    seen = set()
    cnt = 0
    for i, val in enumerate(A):
        if val not in seen:
            seen.add(val)
            cnt += 1
        pref[i] = cnt

    # suffix distinct counts
    suff = [0] * n
    seen.clear()
    cnt = 0
    for i in range(n - 1, -1, -1):
        val = A[i]
        if val not in seen:
            seen.add(val)
            cnt += 1
        suff[i] = cnt

    # segment tree for range add and range max
    size = 1
    while size < n:
        size <<= 1
    seg = [float('-inf')] * (2 * size)
    lazy = [0] * (2 * size)
    # initialize leaves with pref values (positions 0..n-1)
    for i in range(n):
        seg[size + i] = pref[i]
    for i in range(size - 1, 0, -1):
        seg[i] = max(seg[2 * i], seg[2 * i + 1])

    def apply(node, val):
        seg[node] += val
        lazy[node] += val

    def push(node):
        if lazy[node] != 0:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = 0

    # range add [l, r] inclusive
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
            return float('-inf')
        if l <= node_l and node_r <= r:
            return seg[node]
        push(node)
        mid = (node_l + node_r) // 2
        left = query_max(l, r, node * 2, node_l, mid)
        right = query_max(l, r, node * 2 + 1, mid + 1, node_r)
        return left if left > right else right

    last_pos = {}
    answer = 0
    # iterate j as the end index of the middle segment (0-indexed)
    for j in range(1, n - 1):
        val = A[j]
        prev = last_pos.get(val, -1)
        # we need to add 1 to all i where i >= prev (or 0 if prev == -1) and i < j
        l = 0 if prev == -1 else prev
        r = j - 1
        if l <= r:
            range_add(l, r, 1, 1, 0, size - 1)
        last_pos[val] = j
        # best prefix + middle distinct for i in [0, j-1]
        cur_best = query_max(0, j - 1, 1, 0, size - 1)
        candidate = cur_best + suff[j + 1]
        if candidate > answer:
            answer = candidate

    print(answer)

if __name__ == "__main__":
    solve()
