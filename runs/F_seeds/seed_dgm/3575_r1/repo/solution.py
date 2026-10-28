from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # pre[i][j]: set of OR values choosing exactly j elements from nums[:i]
        pre = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        pre[0][0] = {0}
        for i in range(1, n + 1):
            x = nums[i - 1]
            cur, prev = pre[i], pre[i - 1]
            for j in range(k + 1):
                s = set(prev[j])
                if j > 0:
                    for v in prev[j - 1]:
                        s.add(v | x)
                cur[j] = s
        # suf[i][j]: set of OR values choosing exactly j elements from nums[i:]
        suf = [[set() for _ in range(k + 1)] for _ in range(n + 1)]
        suf[n][0] = {0}
        for i in range(n - 1, -1, -1):
            x = nums[i]
            cur, nxt = suf[i], suf[i + 1]
            for j in range(k + 1):
                s = set(nxt[j])
                if j > 0:
                    for v in nxt[j - 1]:
                        s.add(v | x)
                cur[j] = s
        best = 0
        for i in range(k, n - k + 1):
            left = pre[i][k]
            right = suf[i][k]
            for a in left:
                for b in right:
                    if a ^ b > best:
                        best = a ^ b
        return best
