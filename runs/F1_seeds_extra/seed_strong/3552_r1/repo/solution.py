from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # pw[j] = 10^j mod k
        pw = [0] * n
        pw[0] = 1 % k
        for j in range(1, n):
            pw[j] = pw[j - 1] * 10 % k

        full = (1 << k) - 1

        def shift_mask(mask: int, s: int) -> int:
            # residues r in mask -> (r + s) mod k
            s %= k
            return ((mask << s) | (mask >> (k - s))) & full

        # weights for half positions
        w = [0] * h
        for i in range(h):
            j = n - 1 - i
            if j == i:
                w[i] = pw[j]
            else:
                w[i] = (pw[j] + pw[i]) % k

        # reach[i] = bitmask of residues achievable by positions i..h-1 (digits 0..9,
        # with position 0 restricted to 1..9)
        cache = {}

        def step(mask: int, wi: int, lo: int) -> int:
            key = (mask, wi, lo)
            v = cache.get(key)
            if v is None:
                v = 0
                for d in range(lo, 10):
                    v |= shift_mask(mask, d * wi)
                cache[key] = v
            return v

        reach = [0] * (h + 1)
        reach[h] = 1  # only residue 0
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            reach[i] = step(reach[i + 1], w[i], lo)

        # need residue 0 total; greedy from the front
        if not (reach[0] >> 0) & 1:
            return ""
        cur = 0
        digits = []
        for i in range(h):
            lo = 1 if i == 0 else 0
            chosen = -1
            for d in range(9, lo - 1, -1):
                nxt = (cur - d * w[i]) % k
                if (reach[i + 1] >> nxt) & 1:
                    chosen = d
                    cur = nxt
                    break
            if chosen < 0:
                return ""
            digits.append(chosen)

        half = [str(d) for d in digits]
        if n % 2 == 0:
            tail = half[::-1]
        else:
            tail = half[-2::-1]
        return "".join(half) + "".join(tail)
