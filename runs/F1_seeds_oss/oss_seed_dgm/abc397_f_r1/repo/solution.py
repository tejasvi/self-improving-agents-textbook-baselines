# Solution for Variety Split Hard
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0] + [int(next(it)) for _ in range(N)]  # 1-indexed

    # prefix distinct counts
    pref = [0] * (N + 1)
    seen = set()
    cnt = 0
    for i in range(1, N + 1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        pref[i] = cnt

    # suffix distinct counts
    suff = [0] * (N + 2)
    seen.clear()
    cnt = 0
    for i in range(N, 0, -1):
        if A[i] not in seen:
            seen.add(A[i])
            cnt += 1
        suff[i] = cnt

    # segment tree supporting range add and range max
    INF_NEG = -10 ** 9
    size = N  # indices 1..N
    seg = [INF_NEG] * (4 * size)
    lazy = [0] * (4 * size)

    def build(node, l, r):
        if l == r:
            # i must allow at least one element in middle and right parts -> i <= N-2
            seg[node] = pref[l] if l <= N - 2 else INF_NEG
            return
        m = (l + r) // 2
        build(node * 2, l, m)
        build(node * 2 + 1, m + 1, r)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def push(node):
        if lazy[node] != 0:
            for child in (node * 2, node * 2 + 1):
                seg[child] += lazy[node]
                lazy[child] += lazy[node]
            lazy[node] = 0

    def range_add(node, l, r, ql, qr, val):
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            seg[node] += val
            lazy[node] += val
            return
        push(node)
        m = (l + r) // 2
        range_add(node * 2, l, m, ql, qr, val)
        range_add(node * 2 + 1, m + 1, r, ql, qr, val)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def range_max(node, l, r, ql, qr):
        if ql > r or qr < l:
            return INF_NEG
        if ql <= l and r <= qr:
            return seg[node]
        push(node)
        m = (l + r) // 2
        left = range_max(node * 2, l, m, ql, qr)
        right = range_max(node * 2 + 1, m + 1, r, ql, qr)
        return max(left, right)

    build(1, 1, size)

    last_pos = [0] * (N + 1)  # values are between 1 and N
    answer = 0

    # iterate j = end index of the middle part (2 <= j <= N-1)
    for j in range(2, N):
        # incorporate A[j] into the middle part for future queries
        val = A[j]
        prev = last_pos[val]
        if prev == 0:
            left = 1
        else:
            left = prev
        right = j - 1
        if left <= right:
            range_add(1, 1, size, left, right, 1)
        last_pos[val] = j

        # now seg[i] = pref[i] + distinct(i+1..j) for all i
        best_left = range_max(1, 1, size, 1, j - 1)
        total = best_left + suff[j + 1]
        if total > answer:
            answer = total

    print(answer)

if __name__ == "__main__":
    solve()
