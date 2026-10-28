class Solution:
    def minStartingIndex(self, s: str, pattern: str) -> int:
        n, m = len(s), len(pattern)
        if m > n:
            return -1

        # Z-function on pattern + sep + s gives, for each i, the LCP of s[i:] with pattern.
        t = pattern + "#" + s
        L = len(t)
        z = [0] * L
        l = r = 0
        for i in range(1, L):
            if i < r:
                z[i] = min(r - i, z[i - l])
            while i + z[i] < L and t[z[i]] == t[i + z[i]]:
                z[i] += 1
            if i + z[i] > r:
                l, r = i, i + z[i]

        # Polynomial hashing for O(1) substring comparison.
        MOD = (1 << 61) - 1
        BASE = 131542391

        def build(x):
            h = [0] * (len(x) + 1)
            for i, ch in enumerate(x):
                h[i + 1] = (h[i] * BASE + ord(ch)) % MOD
            return h

        ph = build(pattern)
        sh = build(s)
        pw = [1] * (max(n, m) + 1)
        for i in range(1, len(pw)):
            pw[i] = pw[i - 1] * BASE % MOD

        def get(h, a, b):
            return (h[b] - h[a] * pw[b - a]) % MOD

        for i in range(n - m + 1):
            lcp = z[m + 1 + i]
            if lcp >= m:
                return i
            # first mismatch at offset lcp; the remainder must match exactly
            j = lcp + 1
            if j >= m:
                return i
            if get(sh, i + j, i + m) == get(ph, j, m):
                return i
        return -1
