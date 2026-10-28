from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # Helper function to compute the square‑free kernel of a number.
        # The kernel is the product of primes that appear with odd exponent
        # in the prime factorisation of the number.
        def kernel(x: int) -> int:
            res = 1
            n = x
            # trial division using pre‑computed primes up to sqrt(1e9)
            for p in primes:
                if p * p > n:
                    break
                cnt = 0
                while n % p == 0:
                    n //= p
                    cnt ^= 1  # keep only parity (0 even, 1 odd)
                if cnt:
                    res *= p
            # if remainder is a prime > sqrt(original) it appears once
            if n > 1:
                res *= n
            return res

        # Sieve primes up to sqrt(1e9) ~ 31623
        limit = int(1e5)  # safe upper bound, but we only need up to 31623
        # We'll generate primes lazily only once.
        global _primes_cache
        try:
            primes = _primes_cache
        except NameError:
            # Generate primes up to 31623 using simple sieve
            max_p = 31623
            sieve = bytearray(b'\x01') * (max_p + 1)
            sieve[0:2] = b'\x00\x00'
            for i in range(2, int(max_p ** 0.5) + 1):
                if sieve[i]:
                    step = i
                    start = i * i
                    sieve[start:max_p+1:step] = b'\x00' * ((max_p - start)//step + 1)
            primes = [i for i, is_prime in enumerate(sieve) if is_prime]
            _primes_cache = primes

        # Group sums by kernel
        sum_by_kernel = {}
        for val in nums:
            k = kernel(val)
            sum_by_kernel[k] = sum_by_kernel.get(k, 0) + val
        # The answer is the maximum group sum (single elements are naturally considered)
        return max(sum_by_kernel.values())
