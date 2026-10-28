# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    H = [0] + [int(next(it)) for _ in range(N)]  # 1-indexed
    # Compute previous greater element for each position (nearest to the left with higher height)
    prev_greater = [0] * (N + 1)
    stack = []  # monotonic decreasing stack of indices (heights decreasing)
    for i in range(1, N + 1):
        while stack and H[stack[-1]] < H[i]:
            stack.pop()
        prev_greater[i] = stack[-1] if stack else 0
        stack.append(i)
    # For each building k, it can be seen from a building i (i<k) iff prev_greater[k] <= i.
    # We need for each query (l, r): count k > r with prev_greater[k] <= l.
    # Process offline by sorting buildings descending by index and queries descending by r.
    points = [(k, prev_greater[k]) for k in range(1, N + 1)]
    points.sort(key=lambda x: -x[0])  # descending k
    queries = []
    for idx in range(Q):
        l = int(next(it))
        r = int(next(it))
        queries.append((r, l, idx))
    queries.sort(key=lambda x: -x[0])  # descending r
    # BIT over prev_greater values (0..N). We'll store at position y+1 to handle y=0.
    size = N + 3
    bit = [0] * size
    def bit_add(pos, delta=1):
        while pos < size:
            bit[pos] += delta
            pos += pos & -pos
    def bit_sum(pos):
        s = 0
        while pos > 0:
            s += bit[pos]
            pos -= pos & -pos
        return s
    ans = [0] * Q
    p = 0
    for r, l, qid in queries:
        while p < len(points) and points[p][0] > r:
            _, y = points[p]
            bit_add(y + 1)
            p += 1
        # count of y <= l among added points
        ans[qid] = bit_sum(l + 1)
    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
