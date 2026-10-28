from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def extend(cur, x):
            # cur[j] = set of OR values using exactly j chosen elements
            new = [set(s) for s in cur]
            for j in range(1, k + 1):
                if cur[j - 1]:
                    new[j].update(v | x for v in cur[j - 1])
            return new

        # prefix[i][k]: OR values choosing k elements from nums[:i]
        prefix = [None] * (n + 1)
        cur = [set() for _ in range(k + 1)]
        cur[0].add(0)
        prefix[0] = cur
        for i in range(1, n + 1):
            cur = extend(cur, nums[i - 1])
            prefix[i] = cur

        best = 0
        # suf[j]: OR values choosing j elements from nums[i:]
        suf = [set() for _ in range(k + 1)]
        suf[0].add(0)
        for i in range(n, -1, -1):
            if i < n:
                suf = extend(suf, nums[i])
            left = prefix[i][k]
            right = suf[k]
            if left and right:
                for a in left:
                    for b in right:
                        if a ^ b > best:
                            best = a ^ b
        return best
