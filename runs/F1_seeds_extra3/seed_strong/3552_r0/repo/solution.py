from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        full = (1 << k) - 1

        def rot(mask: int, s: int) -> int:
            # shift every residue x in mask to (x + s) mod k
            s %= k
            if s == 0:
                return mask
            return ((mask << s) | (mask >> (k - s))) & full

        h = (n + 1) // 2
        # weight of half-digit i (place values i and n-1-i from the right)
        def weight(i: int) -> int:
            j = n - 1 - i
            if i == j:
                return pow(10, i, k) % k
            return (pow(10, i, k) + pow(10, j, k)) % k

        # trans[w][mask] = union over d in 0..9 of rot(mask, d*w)
        # trans0[w][mask] = same but d in 1..9 (leading digit)
        trans = [[0] * (1 << k) for _ in range(k)]
        trans0 = [[0] * (1 << k) for _ in range(k)]
        for w in range(k):
            for m in range(1 << k):
                a = 0
                b = 0
                for d in range(10):
                    r = rot(m, d * w)
                    a |= r
                    if d >= 1:
                        b |= r
                trans[w][m] = a
                trans0[w][m] = b

        ws = [weight(i) for i in range(h)]
        # T[i] = set of residues achievable by digits i..h-1
        T = [0] * (h + 1)
        T[h] = 1  # only residue 0
        for i in range(h - 1, -1, -1):
            if i == 0:
                T[i] = trans0[ws[i]][T[i + 1]]
            else:
                T[i] = trans[ws[i]][T[i + 1]]

        if not (T[0] >> 0) & 1:
            return ""

        digits = []
        p = 0  # residue of prefix sum so far
        for i in range(h):
            w = ws[i]
            lo = 1 if i == 0 else 0
            chosen = -1
            for d in range(9, lo - 1, -1):
                np_ = (p + d * w) % k
                need = (-np_) % k
                if (T[i + 1] >> need) & 1:
                    chosen = d
                    p = np_
                    break
            if chosen < 0:
                return ""
            digits.append(chosen)

        left = digits
        if n % 2 == 1:
            right = left[:-1][::-1]
        else:
            right = left[::-1]
        return "".join(str(d) for d in left + right)
