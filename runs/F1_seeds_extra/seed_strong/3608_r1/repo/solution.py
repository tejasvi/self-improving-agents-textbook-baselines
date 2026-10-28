from typing import *
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        M = max(nums)
        n = len(nums)
        # cnt[m] = number of elements divisible by m
        freq = [0] * (M + 1)
        for x in nums:
            freq[x] += 1
        cnt = [0] * (M + 1)
        for m in range(1, M + 1):
            cnt[m] = sum(freq[k] for k in range(m, M + 1, m))
        # Mobius function up to M
        mu = [1] * (M + 1)
        is_p = [True] * (M + 1)
        for p in range(2, M + 1):
            if is_p[p]:
                for k in range(p, M + 1, p):
                    if k > p:
                        is_p[k] = False
                    mu[k] = -mu[k]
                pp = p * p
                for k in range(pp, M + 1, pp):
                    mu[k] = 0
        pow2 = [1] * (2 * n + 2)
        pow3 = [1] * (n + 1)
        for i in range(1, 2 * n + 2):
            pow2[i] = pow2[i - 1] * 2 % MOD
        for i in range(1, n + 1):
            pow3[i] = pow3[i - 1] * 3 % MOD

        def N(x, y):
            # pairs (S1, S2) disjoint, nonempty, S1 subset of multiples of x, S2 subset of multiples of y
            c1 = cnt[x] if x <= M else 0
            c2 = cnt[y] if y <= M else 0
            l = x * y // gcd(x, y)
            c12 = cnt[l] if l <= M else 0
            t = pow3[c12] * pow2[c1 + c2 - 2 * c12] - pow2[c1] - pow2[c2] + 1
            return t % MOD

        ans = 0
        for g in range(1, M + 1):
            K = M // g
            e = 0
            for a in range(1, K + 1):
                if mu[a] == 0:
                    continue
                for b in range(1, K + 1):
                    if mu[b] == 0:
                        continue
                    e += mu[a] * mu[b] * N(g * a, g * b)
            ans = (ans + e) % MOD
        return ans % MOD
