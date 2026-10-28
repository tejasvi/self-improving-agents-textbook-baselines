# Solution for Variety Split Hard problem.
# Computes maximum sum of distinct counts in three contiguous subarrays.
# Uses segment tree with lazy propagation to maintain max over (pref[i] + distinct(i+1..j)).

import sys

class SegTree:
    def __init__(self, data):
        n = len(data)
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.size = self.N * 2
        self.maxv = [-10**9] * self.size
        self.lazy = [0] * self.size
        for i, val in enumerate(data):
            self.maxv[self.N + i] = val
        for i in range(self.N - 1, 0, -1):
            self.maxv[i] = max(self.maxv[i << 1], self.maxv[(i << 1) | 1])

    def _push(self, idx):
        if self.lazy[idx] != 0:
            for child in (idx << 1, (idx << 1) | 1):
                self.maxv[child] += self.lazy[idx]
                self.lazy[child] += self.lazy[idx]
            self.lazy[idx] = 0

    def _add(self, l, r, val, idx, left, right):
        if left > right:
            return
        if r < left or right < l:
            return
        if l <= left and right <= r:
            self.maxv[idx] += val
            self.lazy[idx] += val
            return
        self._push(idx)
        mid = (left + right) >> 1
        self._add(l, r, val, idx << 1, left, mid)
        self._add(l, r, val, (idx << 1) | 1, mid + 1, right)
        self.maxv[idx] = max(self.maxv[idx << 1], self.maxv[(idx << 1) | 1])

    def range_add(self, l, r, val):
        if l > r:
            return
        self._add(l, r, val, 1, 0, self.N - 1)

    def _query(self, l, r, idx, left, right):
        if left > right:
            return -10**9
        if r < left or right < l:
            return -10**9
        if l <= left and right <= r:
            return self.maxv[idx]
        self._push(idx)
        mid = (left + right) >> 1
        return max(self._query(l, r, idx << 1, left, mid),
                   self._query(l, r, (idx << 1) | 1, mid + 1, right))

    def range_max(self, l, r):
        if l > r:
            return -10**9
        return self._query(l, r, 1, 0, self.N - 1)


def solve():
    print('debug start', file=sys.stderr)
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    pref = [0] * (N + 1)
    seen = set()
    for i in range(1, N + 1):
        seen.add(A[i - 1])
        pref[i] = len(seen)
    suff = [0] * (N + 2)
    seen.clear()
    for i in range(N, 0, -1):
        seen.add(A[i - 1])
        suff[i] = len(seen)
    seg = SegTree(pref)
    last_pos = {}
    ans = 0
    for j in range(1, N + 1):
        val = A[j - 1]
        prev = last_pos.get(val, 0)
        seg.range_add(prev, j - 1, 1)
        last_pos[val] = j
        if 2 <= j <= N - 1:
            best = seg.range_max(1, j - 1)
            total = best + suff[j + 1]
            if total > ans:
                ans = total
    print(ans)

if __name__ == "__main__":
    solve()
