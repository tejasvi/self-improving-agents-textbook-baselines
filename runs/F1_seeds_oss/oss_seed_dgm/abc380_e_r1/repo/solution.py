# Write your solution here. Read from stdin, write to stdout.

import sys
sys.setrecursionlimit(1 << 25)

class SegmentTree:
    def __init__(self, n, init_vals):
        self.n = n
        size = 4 * n
        self.col = [0] * size  # uniform color of segment, 0 means mixed
        self.lazy = [0] * size  # pending assignment, 0 = none
        self.build(1, 1, n, init_vals)

    def build(self, idx, l, r, init_vals):
        if l == r:
            self.col[idx] = init_vals[l]
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m, init_vals)
        self.build(idx * 2 + 1, m + 1, r, init_vals)
        left = self.col[idx * 2]
        right = self.col[idx * 2 + 1]
        self.col[idx] = left if left == right else 0

    def push(self, idx, l, r):
        if self.lazy[idx]:
            val = self.lazy[idx]
            self.col[idx] = val
            if l != r:
                self.lazy[idx * 2] = val
                self.lazy[idx * 2 + 1] = val
            self.lazy[idx] = 0

    def range_assign(self, ql, qr, val):
        self._range_assign(1, 1, self.n, ql, qr, val)

    def _range_assign(self, idx, l, r, ql, qr, val):
        self.push(idx, l, r)
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.lazy[idx] = val
            self.push(idx, l, r)
            return
        m = (l + r) // 2
        self._range_assign(idx * 2, l, m, ql, qr, val)
        self._range_assign(idx * 2 + 1, m + 1, r, ql, qr, val)
        left = self.col[idx * 2]
        right = self.col[idx * 2 + 1]
        self.col[idx] = left if left == right else 0

    def point_query(self, pos):
        return self._point_query(1, 1, self.n, pos)

    def _point_query(self, idx, l, r, pos):
        self.push(idx, l, r)
        if l == r:
            return self.col[idx]
        m = (l + r) // 2
        if pos <= m:
            return self._point_query(idx * 2, l, m, pos)
        else:
            return self._point_query(idx * 2 + 1, m + 1, r, pos)

    # returns uniform color of [ql, qr] if whole interval has same color, else 0
    def range_color(self, ql, qr):
        return self._range_color(1, 1, self.n, ql, qr)

    def _range_color(self, idx, l, r, ql, qr):
        self.push(idx, l, r)
        if qr < l or r < ql:
            return -1  # outside, treat as neutral
        if ql <= l and r <= qr:
            return self.col[idx]
        m = (l + r) // 2
        left = self._range_color(idx * 2, l, m, ql, qr)
        right = self._range_color(idx * 2 + 1, m + 1, r, ql, qr)
        if left == -1:
            return right
        if right == -1:
            return left
        return left if left == right else 0

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    # initial colors: cell i has color i
    init = [0] * (N + 1)
    for i in range(1, N + 1):
        init[i] = i
    seg = SegmentTree(N, init)
    # counts per color (1..N)
    cnt = [0] * (N + 1)
    for i in range(1, N + 1):
        cnt[i] = 1

    out_lines = []
    for _ in range(Q):
        typ = int(next(it))
        if typ == 1:
            x = int(next(it))
            c = int(next(it))
            cur = seg.point_query(x)
            if cur == c:
                continue
            # find left boundary L where all colors are cur
            lo, hi = 1, x
            while lo < hi:
                mid = (lo + hi) // 2
                col = seg.range_color(mid, x)
                if col == cur:
                    hi = mid
                else:
                    lo = mid + 1
            L = lo
            # find right boundary R
            lo, hi = x, N
            while lo < hi:
                mid = (lo + hi + 1) // 2
                col = seg.range_color(x, mid)
                if col == cur:
                    lo = mid
                else:
                    hi = mid - 1
            R = lo
            length = R - L + 1
            cnt[cur] -= length
            cnt[c] += length
            seg.range_assign(L, R, c)
        else:  # typ == 2
            c = int(next(it))
            out_lines.append(str(cnt[c]))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()
