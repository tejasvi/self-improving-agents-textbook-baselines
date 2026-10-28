class Solution:
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        MOD = 10 ** 9 + 7
        L = len(s)

        # Pascal's triangle for binomial coefficients (mod MOD)
        C = [[0] * (L + 1) for _ in range(L + 1)]
        for i in range(L + 1):
            C[i][0] = 1
            for j in range(1, i + 1):
                C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

        # f[m]: number of operations to reduce m to 1 (f[1] = 0)
        def popcount(x: int) -> int:
            return bin(x).count("1")

        f = [0] * (L + 2)
        for m in range(2, L + 2):
            f[m] = 1 + f[popcount(m)]

        # cnt[c]: number of x in [0, n-1] with popcount c
        cnt = [0] * (L + 1)
        ones = 0
        for i, ch in enumerate(s):
            if ch == '1':
                m = L - i - 1  # free bits after placing 0 here
                for c in range(ones, min(L, ones + m) + 1):
                    need = c - ones
                    cnt[c] = (cnt[c] + C[m][need]) % MOD
                ones += 1
        # n itself is not counted (strictly less than n), as the loop only
        # counts numbers that differ from s at a position where s has a 1.

        ans = 0
        for c in range(1, L + 1):
            if c == 1 or f[c] + 1 <= k:
                ans = (ans + cnt[c]) % MOD
        return ans
