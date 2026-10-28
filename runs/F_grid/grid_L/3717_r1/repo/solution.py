from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        INF = float("inf")

        # Coordinate compression of values (by sorted index, ties broken by position).
        order = sorted(range(n), key=lambda i: nums[i])
        rank = [0] * n
        for r, i in enumerate(order):
            rank[i] = r + 1  # 1-based for BIT
        sorted_vals = [nums[i] for i in order]

        size = n
        cnt = [0] * (size + 1)
        sm = [0] * (size + 1)
        LOG = 1
        while (1 << LOG) <= size:
            LOG += 1

        def add(pos, c, v):
            while pos <= size:
                cnt[pos] += c
                sm[pos] += v
                pos += pos & -pos

        def kth(kk):
            # returns 1-based position of kk-th smallest (1-indexed kk)
            pos = 0
            for b in range(LOG, -1, -1):
                np_ = pos + (1 << b)
                if np_ <= size and cnt[np_] < kk:
                    pos = np_
                    kk -= cnt[np_]
            return pos + 1

        def prefix(pos):
            c = s = 0
            while pos > 0:
                c += cnt[pos]
                s += sm[pos]
                pos -= pos & -pos
            return c, s

        # C[st] = min cost to make window [st, st+x-1] equal
        C = [0] * (n - x + 1)
        total_sum = 0
        for i in range(n):
            add(rank[i], 1, nums[i])
            total_sum += nums[i]
            if i >= x:
                j = i - x
                add(rank[j], -1, -nums[j])
                total_sum -= nums[j]
            if i >= x - 1:
                st = i - x + 1
                # median = lower median (x-th smallest with 1-indexed ceil(x/2))
                m_rank = kth((x + 1) // 2)
                med = sorted_vals[m_rank - 1]
                cl, sl = prefix(m_rank)
                # sum of |a - med| = med*cl - sl + (total - sl) - med*(x - cl)
                C[st] = med * cl - sl + (total_sum - sl) - med * (x - cl)

        m = n - x + 1
        # f[p] = min cost using exactly-or-fewer windows within prefix length p
        prev = [0] * (n + 1)  # j = 0
        for _ in range(k):
            cur = [INF] * (n + 1)
            for p in range(x, n + 1):
                best = cur[p - 1]
                cand = prev[p - x] + C[p - x]
                if cand < best:
                    best = cand
                cur[p] = best
            # windows fewer than j are allowed: propagate
            for p in range(1, n + 1):
                if cur[p - 1] < cur[p]:
                    cur[p] = cur[p - 1]
            prev = cur
        return int(prev[n])
