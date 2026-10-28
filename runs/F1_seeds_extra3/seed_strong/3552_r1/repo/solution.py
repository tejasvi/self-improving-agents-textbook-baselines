from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        def rot(m: int, s: int) -> int:
            # rotate k-bit mask m left by s (adds s to every remainder)
            s %= k
            return ((m << s) | (m >> (k - s))) & full

        # weight of position i (0-indexed half position) mod k
        def weight(i: int) -> int:
            j = n - 1 - i
            if i == j:
                return pow(10, i, k)
            return (pow(10, i, k) + pow(10, j, k)) % k

        ws = [weight(i) for i in range(h)]
        # S[i] = bitmask of remainders achievable by positions i..h-1
        S = [0] * (h + 1)
        S[h] = 1  # only remainder 0 with empty suffix
        for i in range(h - 1, -1, -1):
            w = ws[i]
            lo = 1 if i == 0 else 0
            m = 0
            for d in range(lo, 10):
                m |= rot(S[i + 1], d * w)
            S[i] = m

        if not (S[0] & 1):
            return ""

        digits = []
        need = 0  # remainder the suffix (from i) must achieve
        for i in range(h):
            w = ws[i]
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                # need suffix i+1.. to achieve (need - d*w)
                r = (need - d * w) % k
                if (S[i + 1] >> r) & 1:
                    chosen = d
                    need = r
                    break
            digits.append(chosen)

        left = [str(d) for d in digits]
        if n % 2 == 1:
            right = left[-2::-1]
        else:
            right = left[::-1]
        return "".join(left + right)
