from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        # weight of each half-position modulo k
        w = [0] * h
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w[i] = pow(10, i, k) % k
            else:
                w[i] = (pow(10, i, k) + pow(10, j, k)) % k

        def rot(mask, c):
            c %= k
            if c == 0:
                return mask
            return ((mask << c) | (mask >> (k - c))) & full

        # reach[i]: bitmask of residues achievable by positions i..h-1
        reach = [0] * (h + 1)
        reach[h] = 1  # residue 0 only (empty sum)
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            m = 0
            for d in range(lo, 10):
                m |= rot(reach[i + 1], d * w[i])
            reach[i] = m

        digits = [0] * h
        cur = 0  # residue still needed from positions i..h-1 (target = -sum so far)
        # we track the residue of the sum chosen so far; need final total 0
        s = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            for d in range(9, lo - 1, -1):
                ns = (s + d * w[i]) % k
                # need (-ns) mod k reachable by positions i+1..h-1
                need = (-ns) % k
                if (reach[i + 1] >> need) & 1:
                    digits[i] = d
                    s = ns
                    break
            else:
                return ""  # no solution (should not happen)

        res = [0] * n
        for i in range(h):
            res[i] = digits[i]
            res[n - 1 - i] = digits[i]
        return "".join(map(str, res))
