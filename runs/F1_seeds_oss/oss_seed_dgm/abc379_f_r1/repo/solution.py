# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    input = sys.stdin.readline
    first = input().split()
    if not first:
        return
    N, Q = map(int, first)
    H = list(map(int, input().split()))
    # Compute prev_greater: for each i, the nearest index to the left with height > H[i]
    prev_greater = [0] * (N + 1)  # 1-indexed, 0 means none
    stack = []  # decreasing heights (store indices)
    for i in range(1, N + 1):
        h = H[i - 1]
        while stack and H[stack[-1] - 1] < h:
            stack.pop()
        prev_greater[i] = stack[-1] if stack else 0
        stack.append(i)

    # Read queries, store (r, l, idx) and sort by r descending
    queries = []
    for idx in range(Q):
        l, r = map(int, input().split())
        queries.append((r, l, idx))
    queries.sort(reverse=True)

    # Fenwick tree over prev_greater values (0..N). We'll map value v to index v+1.
    size = N + 2
    bit = [0] * (size)
    def bit_add(i, v):
        while i < size:
            bit[i] += v
            i += i & -i
    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    answers = [0] * Q
    cur = N
    qpos = 0
    while qpos < Q:
        r, l, idx = queries[qpos]
        # Insert all positions k where k > r into BIT
        while cur > r:
            pg = prev_greater[cur]
            bit_add(pg + 1, 1)  # shift by 1 because pg can be 0
            cur -= 1
        # For current query, we need count of k > r such that prev_greater[k] <= l
        ans = bit_sum(l + 1)  # because index = pg+1, we need pg <= l => index <= l+1
        answers[idx] = ans
        qpos += 1

    sys.stdout.write('\n'.join(map(str, answers)))

if __name__ == "__main__":
    solve()
