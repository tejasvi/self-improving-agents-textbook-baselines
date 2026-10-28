from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = n // 2
        odd = n % 2 == 1
        # p[j] = 10^j mod k
        p = [0] * n
        p[0] = 1 % k
        for j in range(1, n):
            p[j] = p[j - 1] * 10 % k
        # weight of pair i (outer to inner) and of middle digit
        w = [(p[i] + p[n - 1 - i]) % k for i in range(h)]
        wm = p[h] if odd else 0

        # G[i][r]: from pair index i with current remainder r, completion possible
        G = [None] * (h + 1)
        last = [False] * k
        if odd:
            for r in range(k):
                for d in range(10):
                    if (r + d * wm) % k == 0:
                        last[r] = True
                        break
        else:
            last[0] = True
        G[h] = last
        for i in range(h - 1, -1, -1):
            nxt = G[i + 1]
            cur = [False] * k
            lo = 1 if i == 0 else 0
            wi = w[i]
            for r in range(k):
                for d in range(lo, 10):
                    if nxt[(r + d * wi) % k]:
                        cur[r] = True
                        break
            G[i] = cur

        if not G[0][0]:
            return ""
        digits = [0] * n
        r = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            for d in range(9, lo - 1, -1):
                nr = (r + d * w[i]) % k
                if G[i + 1][nr]:
                    digits[i] = d
                    digits[n - 1 - i] = d
                    r = nr
                    break
        if odd:
            lo = 1 if h == 0 else 0
            for d in range(9, lo - 1, -1):
                if (r + d * wm) % k == 0:
                    digits[h] = d
                    break
        return "".join(map(str, digits))
