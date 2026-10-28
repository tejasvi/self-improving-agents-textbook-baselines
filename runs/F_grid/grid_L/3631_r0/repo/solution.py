MOD = 10**9 + 7


class Solution:
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        L = len(s)

        # g[m] = number of operations needed to reach 1 starting from m (m >= 1)
        g = [0] * (L + 2)
        for m in range(2, L + 2):
            g[m] = 1 + g[bin(m).count("1")]

        # Pascal's triangle modulo MOD
        C = [[0] * (L + 1) for _ in range(L + 1)]
        for i in range(L + 1):
            C[i][0] = 1
            for j in range(1, i + 1):
                C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

        # cnt[c] = number of x in [0, n-1] with popcount c
        cnt = [0] * (L + 1)
        ones = 0
        for i, ch in enumerate(s):
            if ch == '1':
                rem = L - i - 1
                # place 0 here, remaining bits free
                for c in range(ones, ones + rem + 1):
                    if c <= L:
                        cnt[c] = (cnt[c] + C[rem][c - ones]) % MOD
                ones += 1
        # n itself is excluded (strictly less than n)

        ans = 0
        for c in range(1, L + 1):
            if g[c] <= k - 1:
                ans = (ans + cnt[c]) % MOD
        return ans
