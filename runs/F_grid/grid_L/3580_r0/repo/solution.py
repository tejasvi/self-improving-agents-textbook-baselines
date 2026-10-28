import random


class Solution:
    def minStartingIndex(self, s: str, pattern: str) -> int:
        n, m = len(s), len(pattern)
        if m > n:
            return -1
        MOD = (1 << 61) - 1
        B = random.randrange(10 ** 5, MOD - 1)

        def build(t):
            h = [0] * (len(t) + 1)
            for i, c in enumerate(t):
                h[i + 1] = (h[i] * B + ord(c)) % MOD
            return h

        hs = build(s)
        hp = build(pattern)
        pw = [1] * (max(n, m) + 1)
        for i in range(1, len(pw)):
            pw[i] = pw[i - 1] * B % MOD

        def get(h, l, r):  # hash of [l, r)
            return (h[r] - h[l] * pw[r - l]) % MOD

        for i in range(n - m + 1):
            # longest common prefix of s[i:] and pattern, capped at m
            lo, hi = 0, m
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if get(hs, i, i + mid) == get(hp, 0, mid):
                    lo = mid
                else:
                    hi = mid - 1
            l = lo
            if l == m:
                return i
            # skip the single mismatch at offset l, check the rest
            if get(hs, i + l + 1, i + m) == get(hp, l + 1, m):
                return i
        return -1
