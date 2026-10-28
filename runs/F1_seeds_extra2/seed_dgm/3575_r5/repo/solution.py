from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # pre[m][j]: set of OR values achievable by choosing exactly j elements
        # from nums[:m]. Only j in [0, k] matters.
        def build(seq):
            # returns list res where res[i][j] = reachable ORs using j of seq[:i]
            cur = [set() for _ in range(k + 1)]
            cur[0].add(0)
            res = [cur]
            for x in seq:
                new = [s.copy() for s in cur]
                for j in range(1, k + 1):
                    prev = cur[j - 1]
                    if prev:
                        tgt = new[j]
                        for v in prev:
                            tgt.add(v | x)
                cur = new
                res.append(cur)
            return res

        pre = build(nums)
        suf_rev = build(nums[::-1])
        # suffix starting at index m has length n - m; suf_rev[n - m] covers nums[m:]
        best = 0
        for m in range(k, n - k + 1):
            left = pre[m][k]
            right = suf_rev[n - m][k]
            for a in left:
                for b in right:
                    v = a ^ b
                    if v > best:
                        best = v
        return best
