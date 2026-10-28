from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        def rot(m, s):
            # rotate k-bit mask m left by s (mod k)
            s %= k
            if s == 0:
                return m
            return ((m << s) | (m >> (k - s))) & full

        # weights per left-index i
        weights = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w = pow(10, i, k) % k
            else:
                w = (pow(10, i, k) + pow(10, j, k)) % k
            weights.append(w)

        # F[i] = bitmask of achievable residues of sum over positions i..h-1
        F = [0] * (h + 1)
        F[h] = 1  # only residue 0 (empty sum)
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            w = weights[i]
            m = 0
            for d in range(lo, 10):
                m |= rot(F[i + 1], d * w)
            F[i] = m

        if not (F[0] & 1):
            return ""  # should not happen for valid n >= 1 (k <= 9)

        # greedy construction
        digits = [0] * h
        partial = 0  # residue of sum chosen so far
        for i in range(h):
            w = weights[i]
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                # remaining suffix (i+1..) must sum to -(partial + d*w) mod k
                need = (-(partial + d * w)) % k
                if (F[i + 1] >> need) & 1:
                    chosen = d
                    break
            digits[i] = chosen
            partial = (partial + chosen * w) % k

        left = digits
        if n % 2 == 1:
            right = left[:-1][::-1]
        else:
            right = left[::-1]
        return "".join(map(str, left + right))
