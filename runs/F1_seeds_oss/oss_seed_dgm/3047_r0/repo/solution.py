from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # The product of any two numbers being a perfect square is equivalent to
        # all numbers having the same square‑free part. The square‑free part of a
        # number is the product of primes that appear an odd number of times in its
        # prime factorisation.
        # Therefore, we group numbers by their square‑free part and take the sum of
        # each group. The answer is the maximum group sum.

        # Pre‑compute primes up to sqrt(1e9) (~31623) for factorisation.
        limit = int(1e5)  # a safe upper bound for sqrt(1e9) plus margin
        # simple sieve
        sieve = [True] * (limit + 1)
        primes = []
        for i in range(2, limit + 1):
            if sieve[i]:
                primes.append(i)
                if i * i <= limit:
                    for j in range(i * i, limit + 1, i):
                        sieve[j] = False

        def squarefree(x: int) -> int:
            # Compute the product of primes with odd exponent.
            res = 1
            temp = x
            for p in primes:
                if p * p > temp:
                    break
                cnt = 0
                while temp % p == 0:
                    temp //= p
                    cnt ^= 1  # keep parity only
                if cnt:
                    res *= p
            if temp > 1:
                # remaining prime factor with exponent 1 (odd)
                res *= temp
            return res

        group_sum = {}
        for v in nums:
            sf = squarefree(v)
            group_sum[sf] = group_sum.get(sf, 0) + v

        return max(group_sum.values()) if group_sum else 0
