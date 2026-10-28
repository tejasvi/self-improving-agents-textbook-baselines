from typing import List


class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        nums = list(nums)
        # Fenwick tree (1-indexed) over array positions 0..n-1
        tree = [0] * (n + 1)

        def add(pos, delta):
            i = pos + 1
            while i <= n:
                tree[i] += delta
                i += i & (-i)

        def prefix(pos):
            # sum over positions [0, pos]
            i = pos + 1
            s = 0
            while i > 0:
                s += tree[i]
                i -= i & (-i)
            return s

        is_peak = [0] * n

        def is_pk(j):
            return 1 if 0 < j < n - 1 and nums[j] > nums[j - 1] and nums[j] > nums[j + 1] else 0

        for j in range(1, n - 1):
            if is_pk(j):
                is_peak[j] = 1
                add(j, 1)

        answer = []
        for q in queries:
            if q[0] == 1:
                l, r = q[1], q[2]
                if r - l < 2:
                    answer.append(0)
                    continue
                answer.append(prefix(r - 1) - prefix(l))
            else:
                idx, val = q[1], q[2]
                nums[idx] = val
                for j in (idx - 1, idx, idx + 1):
                    if 0 <= j < n:
                        new = is_pk(j)
                        if new != is_peak[j]:
                            is_peak[j] = new
                            add(j, new - (1 - new))  # +1 if became peak, -1 if not
        return answer
