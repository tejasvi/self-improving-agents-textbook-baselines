from typing import List


class Solution:
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        n = len(nums)
        total = n * (n + 1) // 2
        need = (total + 1) // 2  # smallest x with count(<= x) >= need

        # Compress values to 0..m-1 for fast list-based counting.
        idx = {}
        arr = []
        for v in nums:
            if v not in idx:
                idx[v] = len(idx)
            arr.append(idx[v])
        m = len(idx)

        def at_most(k: int) -> int:
            cnt = [0] * m
            distinct = 0
            left = 0
            res = 0
            for right in range(n):
                x = arr[right]
                if cnt[x] == 0:
                    distinct += 1
                cnt[x] += 1
                while distinct > k:
                    y = arr[left]
                    cnt[y] -= 1
                    if cnt[y] == 0:
                        distinct -= 1
                    left += 1
                res += right - left + 1
            return res

        lo, hi = 1, m
        while lo < hi:
            mid = (lo + hi) // 2
            if at_most(mid) >= need:
                hi = mid
            else:
                lo = mid + 1
        return lo
