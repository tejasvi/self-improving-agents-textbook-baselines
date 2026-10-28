from typing import *


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        B = 7
        V = 1 << B
        # NB[b]: bitmask of positions v (0..127) whose bit b is 0
        NB = []
        WB = []
        for b in range(B):
            nb = 0
            for v in range(V):
                if not (v >> b) & 1:
                    nb |= 1 << v
            NB.append(nb)
            WB.append(((1 << V) - 1) ^ nb)

        def or_shift(S, a):
            # set {v | a : v in S}, S as bitmask over values
            for b in range(B):
                if (a >> b) & 1:
                    S = ((S & NB[b]) << (1 << b)) | (S & WB[b])
            return S

        # pre[m][j]: achievable OR values choosing j elements from nums[:m]
        pre = [None] * (n + 1)
        cur = [1] + [0] * k  # bit 0 set: empty OR = 0
        pre[0] = cur
        for i in range(n):
            a = nums[i]
            nxt = cur[:]
            for j in range(1, k + 1):
                if cur[j - 1]:
                    nxt[j] |= or_shift(cur[j - 1], a)
            cur = nxt
            pre[i + 1] = cur
        suf = [None] * (n + 1)
        cur = [1] + [0] * k
        suf[n] = cur
        for i in range(n - 1, -1, -1):
            a = nums[i]
            nxt = cur[:]
            for j in range(1, k + 1):
                if cur[j - 1]:
                    nxt[j] |= or_shift(cur[j - 1], a)
            cur = nxt
            suf[i] = cur

        def members(S):
            res = []
            v = 0
            while S:
                if S & 1:
                    res.append(v)
                S >>= 1
                v += 1
            return res

        def max_xor(X, Y):
            # max x^y over x in X, y in Y (lists of ints < 128)
            ans = 0
            for bit in range(B - 1, -1, -1):
                cand = ans | (1 << bit)
                t = cand >> bit
                prefX = {x >> bit for x in X}
                if any((y >> bit) ^ t in prefX for y in Y):
                    ans = cand
            return ans

        best = 0
        for m in range(k, n - k + 1):
            X = members(pre[m][k])
            Y = members(suf[m][k])
            if X and Y:
                best = max(best, max_xor(X, Y))
        return best
