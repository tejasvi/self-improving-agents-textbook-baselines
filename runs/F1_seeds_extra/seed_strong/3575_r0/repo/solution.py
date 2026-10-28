from typing import *


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        M = 128
        full = (1 << (k + 1)) - 1

        def pass_sets(seq):
            # res[i] = bitmask over values v (0..127) such that some k-subset
            # of seq[:i] has OR == v.
            # dp[v] = bitmask over sizes j where some j-subset has OR v.
            dp = [0] * M
            dp[0] = 1
            res = [0] * (len(seq) + 1)
            for idx, x in enumerate(seq):
                # Snapshot the k-size membership for prefix idx
                m = 0
                for v in range(M):
                    if (dp[v] >> k) & 1:
                        m |= 1 << v
                res[idx] = m
                new = dp[:]
                for v in range(M):
                    d = dp[v]
                    if d:
                        t = v | x
                        new[t] |= (d << 1) & full
                dp = new
            m = 0
            for v in range(M):
                if (dp[v] >> k) & 1:
                    m |= 1 << v
            res[len(seq)] = m
            return res

        L = pass_sets(nums)                 # L[i]: left values from nums[:i]
        R_rev = pass_sets(nums[::-1])       # R_rev[j]: values from last j elements
        # right values from nums[i:] is R_rev[n - i]
        # Build per-value index masks over split points i.
        maskL = [0] * M
        maskR = [0] * M
        for i in range(n + 1):
            lv = L[i]
            rv = R_rev[n - i]
            for v in range(M):
                if (lv >> v) & 1:
                    maskL[v] |= 1 << i
                if (rv >> v) & 1:
                    maskR[v] |= 1 << i
        best = -1
        for a in range(M):
            if not maskL[a]:
                continue
            for b in range(M):
                if maskR[b] and (maskL[a] & maskR[b]):
                    val = a ^ b
                    if val > best:
                        best = val
        return best
