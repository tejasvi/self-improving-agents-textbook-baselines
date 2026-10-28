from typing import *

W = 128  # values are < 2^7, so OR/XOR results lie in [0, 128)

# L[b]: bitset of indices v in [0,128) with bit b clear
# H[b]: bitset of indices v in [0,128) with bit b set
L = [0] * 7
H = [0] * 7
for b in range(7):
    for v in range(W):
        if v >> b & 1:
            H[b] |= 1 << v
        else:
            L[b] |= 1 << v
FULL = (1 << W) - 1


def or_shift(B: int, x: int) -> int:
    """Return bitset {v | x : v in B}."""
    for b in range(7):
        if x >> b & 1:
            B = (B & H[b]) | ((B & L[b]) << (1 << b))
    return B


def xor_shift(B: int, a: int) -> int:
    """Return bitset {v ^ a : v in B}."""
    for c in range(7):
        if a >> c & 1:
            s = 1 << c
            B = ((B & L[c]) << s) | ((B & H[c]) >> s)
    return B


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # pre[i][j]: bitset of OR values of j-element subsequences of nums[:i]
        pre = [None] * (n + 1)
        dp = [0] * (k + 1)
        dp[0] = 1  # OR of empty set = 0
        pre[0] = dp[k]
        for i, x in enumerate(nums):
            for j in range(min(k, i + 1), 0, -1):
                if dp[j - 1]:
                    dp[j] |= or_shift(dp[j - 1], x)
            pre[i + 1] = dp[k]

        # suf[i][j]: bitset of OR values of j-element subsequences of nums[i:]
        suf = [0] * (n + 1)
        dp = [0] * (k + 1)
        dp[0] = 1
        suf[n] = dp[k]
        cnt = 0
        for i in range(n - 1, -1, -1):
            x = nums[i]
            cnt += 1
            for j in range(min(k, cnt), 0, -1):
                if dp[j - 1]:
                    dp[j] |= or_shift(dp[j - 1], x)
            suf[i] = dp[k]

        best = 0
        for i in range(k, n - k + 1):
            P = pre[i]
            S = suf[i]
            if not P or not S:
                continue
            # T = { a ^ b : a in P, b in S }
            T = 0
            a_bits = P
            while a_bits:
                low = a_bits & -a_bits
                a = low.bit_length() - 1
                T |= xor_shift(S, a)
                a_bits ^= low
            if T:
                cand = T.bit_length() - 1
                if cand > best:
                    best = cand
        return best
