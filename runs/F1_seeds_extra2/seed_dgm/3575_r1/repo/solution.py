from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def bits_of(mask):
            res = []
            v = 0
            while mask:
                if mask & 1:
                    res.append(v)
                mask >>= 1
                v += 1
            return res

        def build(seq):
            # res[i][j] = bitmask of OR values achievable by choosing exactly j
            # elements from seq[:i]
            m = len(seq)
            dp = [0] * (k + 1)
            dp[0] = 1  # OR value 0 with zero elements
            res = [None] * (m + 1)
            res[0] = dp[:]
            for i, x in enumerate(seq):
                new = dp[:]
                for j in range(1, k + 1):
                    if dp[j - 1]:
                        add = 0
                        for v in bits_of(dp[j - 1]):
                            add |= 1 << (v | x)
                        new[j] |= add
                dp = new
                res[i + 1] = dp[:]
            return res

        pre = build(nums)
        suf_rev = build(nums[::-1])  # suf_rev[t][k] covers last t elements
        best = -1
        for i in range(k, n - k + 1):
            # left: exactly k from nums[:i]; right: exactly k from nums[i:]
            L = bits_of(pre[i][k])
            R = bits_of(suf_rev[n - i][k])
            for a in L:
                for b in R:
                    c = a ^ b
                    if c > best:
                        best = c
        return best
