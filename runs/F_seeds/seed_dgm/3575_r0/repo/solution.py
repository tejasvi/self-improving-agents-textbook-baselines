from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def shift_or(bits, x):
            # {v | x : v in bits}, bits is a 128-bit mask
            res = 0
            v = 0
            b = bits
            while b:
                if b & 1:
                    res |= 1 << (v | x)
                b >>= 1
                v += 1
            return res

        def reach(seq):
            # res[i] = bitmask of OR values from choosing exactly k elements of seq[:i]
            res = [0] * (n + 1)
            dp = [0] * (k + 1)
            dp[0] = 1  # OR value 0 with zero elements
            res[0] = dp[k]
            for i, x in enumerate(seq):
                for j in range(min(k, i + 1), 0, -1):
                    if dp[j - 1]:
                        dp[j] |= shift_or(dp[j - 1], x)
                res[i + 1] = dp[k]
            return res

        pre = reach(nums)
        suf = reach(nums[::-1])  # suf[m]: ORs from last m elements

        def members(mask):
            out = []
            v = 0
            while mask:
                if mask & 1:
                    out.append(v)
                mask >>= 1
                v += 1
            return out

        best = -1
        for p in range(k, n - k + 1):
            L = members(pre[p])
            R = members(suf[n - p])
            for a in L:
                for b in R:
                    if a ^ b > best:
                        best = a ^ b
        return best
