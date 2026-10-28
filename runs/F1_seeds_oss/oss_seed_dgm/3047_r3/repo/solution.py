from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # Helper to compute the square‑free part of a number.
        # The square‑free part is the product of primes that appear with an odd exponent in the factorisation.
        def squarefree(x: int) -> int:
            # Factorise using trial division by primes up to sqrt(x).
            sf = 1
            n = x
            for p in primes:
                if p * p > n:
                    break
                cnt = 0
                while n % p == 0:
                    n //= p
                    cnt ^= 1  # toggle parity
                if cnt:
                    sf *= p
            # If a prime factor > sqrt(original) remains, it appears exactly once.
            if n > 1:
                sf *= n
            return sf

        # Generate primes up to sqrt(1e9) ≈ 31623.
        limit = int(1e5)  # safe upper bound; we will trim later.
        # Actually we only need up to sqrt(max(nums)). Compute precise bound.
        max_num = max(nums) if nums else 0
        import math
        bound = int(math.isqrt(max_num)) + 1
        sieve = bytearray(b'\x01') * (bound + 1)
        sieve[0:2] = b'\x00\x00'
        for i in range(2, int(bound ** 0.5) + 1):
            if sieve[i]:
                step = i
                start = i * i
                sieve[start:bound+1:step] = b'\x00' * ((bound - start) // step + 1)
        primes = [i for i, is_prime in enumerate(sieve) if is_prime]

        group_sum = {}
        max_total = 0
        for v in nums:
            sf = squarefree(v)
            new_sum = group_sum.get(sf, 0) + v
            group_sum[sf] = new_sum
            if new_sum > max_total:
                max_total = new_sum
        return max_total
