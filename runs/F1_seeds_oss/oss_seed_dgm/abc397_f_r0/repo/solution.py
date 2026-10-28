# Solution for Variety Split Hard
import sys

INF_NEG = -10**9

class SegTree:
    def __init__(self, init):
        n = len(init)
        self.N = 1
        while self.N < n:
            self.N <<= 1
        self.data = [INF_NEG] * (2 * self.N)
        self.lazy = [0] * (2 * self.N)
        # set leaves
        for i in range(n):
            self.data[self.N + i] = init[i]
        for i in range(self.N - 1, 0, -1):
            self.data[i] = max(self.data[2 * i], self.data[2 * i + 1])

    def _apply(self, idx, val):
        self.data[idx] += val
        self.lazy[idx] += val

    def _push(self, idx):
        if self.lazy[idx] != 0:
            self._apply(2 * idx, self.lazy[idx])
            self._apply(2 * idx + 1, self.lazy[idx])
            self.lazy[idx] = 0

    def _add(self, l, r, val, idx, left, right):
        if r < left or right < l:
            return
        if l <= left and right <= r:
            self._apply(idx, val)
            return
        self._push(idx)
        mid = (left + right) // 2
        self._add(l, r, val, 2 * idx, left, mid)
        self._add(l, r, val, 2 * idx + 1, mid + 1, right)
        self.data[idx] = max(self.data[2 * idx], self.data[2 * idx + 1])

    def add(self, l, r, val):
        if l > r:
            return
        self._add(l, r, val, 1, 0, self.N - 1)

    def _query(self, l, r, idx, left, right):
        if r < left or right < l:
            return INF_NEG
        if l <= left and right <= r:
            return self.data[idx]
        self._push(idx)
        mid = (left + right) // 2
        return max(
            self._query(l, r, 2 * idx, left, mid),
            self._query(l, r, 2 * idx + 1, mid + 1, right)
        )

    def query(self, l, r):
        if l > r:
            return INF_NEG
        return self._query(l, r, 1, 0, self.N - 1)


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # prefix distinct counts dp1[i] = distinct in A[0..i]
    seen = [False] * (N + 1)
    dp1 = [0] * N
    cnt = 0
    for i, v in enumerate(A):
        if not seen[v]:
            seen[v] = True
            cnt += 1
        dp1[i] = cnt

    # DP for two parts: dp2[j] = max_{i<j} (dp1[i] + distinct in A[i+1..j])
    seg = SegTree(dp1)  # holds current dp1[i] + distinct(i+1..current_j)
    last = [-1] * (N + 1)
    dp2 = [INF_NEG] * N
    for j, v in enumerate(A):
        prev = last[v]
        # range of i where A[j] is new in the second part is [prev, j-1]
        l = 0 if prev == -1 else prev
        r = j - 1
        if l <= r:
            seg.add(l, r, 1)
        if j > 0:
            dp2[j] = seg.query(0, j - 1)
        last[v] = j

    # DP for three parts: dp3[k] = max_{j<k} (dp2[j] + distinct in A[j+1..k])
    seg2 = SegTree(dp2)
    last = [-1] * (N + 1)
    dp3 = [INF_NEG] * N
    for k, v in enumerate(A):
        prev = last[v]
        l = 0 if prev == -1 else prev
        r = k - 1
        if l <= r:
            seg2.add(l, r, 1)
        if k > 0:
            dp3[k] = seg2.query(0, k - 1)
        last[v] = k

    # The answer is dp3[N-1] (third part is non‑empty by construction)
    print(dp3[N - 1])

if __name__ == "__main__":
    solve()
