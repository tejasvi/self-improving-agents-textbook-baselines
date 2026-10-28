from typing import *
from math import gcd


class Solution:
    def subsequencePairCount(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        M = max(nums)
        n = len(nums)
        cnt = [0] * (M + 1)
        for x in nums:
            cnt[x] += 1
        # div[d] = number of elements divisible by d
        div = [0] * (M + 1)
        for d in range(1, M + 1):
            s = 0
            for m in range(d, M + 1, d):
                s += cnt[m]
            div[d] = s
        # Mobius function
        mu = [1] * (M + 1)
        is_prime = [True] * (M + 1)
        for p in range(2, M + 1):
            if is_prime[p]:
                for m in range(p, M + 1, p):
                    if m > p:
                        is_prime[m] = False
                    mu[m] = -mu[m]
                pp = p * p
                for m in range(pp, M + 1, pp):
                    mu[m] = 0
        pow2 = [1] * (n + 1)
        pow3 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow2[i] = pow2[i - 1] * 2 % MOD
            pow3[i] = pow3[i - 1] * 3 % MOD

        def H(a, b):
            # pairs (A,B) disjoint nonempty, A subset of multiples of a, B subset of multiples of b
            if a > M or b > M:
                return 0
            l = a * b // gcd(a, b)
            c = div[l] if l <= M else 0
            p = div[a] - c
            q = div[b] - c
            return (pow3[c] * pow2[p + q] - pow2[c + q] - pow2[c + p] + 1) % MOD

        ans = 0
        for g in range(1, M + 1):
            if div[g] < 2:
                continue
            total = 0
            k = M // g
            for i in range(1, k + 1):
                if mu[i] == 0:
                    continue
                for j in range(1, k + 1):
                    if mu[j] == 0:
                        continue
                    total += mu[i] * mu[j] * H(g * i, g * j)
            ans = (ans + total) % MOD
        return ans % MOD
