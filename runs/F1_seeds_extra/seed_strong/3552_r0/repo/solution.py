from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        def rot(m, c):
            if c == 0:
                return m
            return ((m << c) | (m >> (k - c))) & full

        # weight of position i in the half (residue contribution per unit digit)
        def weight(i):
            j = n - 1 - i
            if i == j:
                return pow(10, i, k)
            return (pow(10, i, k) + pow(10, j, k)) % k

        def digits(i):
            return range(1, 10) if i == 0 else range(0, 10)

        # reach[i] = bitmask of residues achievable by positions i..h-1
        reach = [0] * (h + 1)
        reach[h] = 1  # residue 0 only (empty sum)
        for i in range(h - 1, -1, -1):
            w = weight(i)
            m = 0
            for d in digits(i):
                m |= rot(reach[i + 1], (d * w) % k)
            reach[i] = m

        # reach[0] must contain residue 0 (guaranteed by problem)
        target = 0  # residue still needed from positions i..h-1
        half = []
        for i in range(h):
            w = weight(i)
            chosen = None
            for d in sorted(digits(i), reverse=True):
                c = (d * w) % k
                # need (target - c) mod k reachable by positions i+1..h-1
                need = (target - c) % k
                if (reach[i + 1] >> need) & 1:
                    chosen = d
                    target = need
                    break
            half.append(chosen)

        s = [str(d) for d in half]
        left = "".join(s)
        if n % 2 == 1:
            res = left + left[-2::-1]
        else:
            res = left + left[::-1]
        return res
