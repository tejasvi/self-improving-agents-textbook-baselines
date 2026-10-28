from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """Return the maximum sum of a subset where the product of any two
        elements is a perfect square.

        Observation:
        For a number a, write a = s * t^2 where s is square‑free (product of
        primes with odd exponent) and t is an integer.  For two numbers a and b
        we have
            a * b = (s_a * s_b) * (t_a * t_b)^2.
        The product is a perfect square iff s_a * s_b is a perfect square.
        Since s_a and s_b are square‑free, their product is a perfect square
        exactly when s_a == s_b.  Therefore all numbers in a valid subset must
        share the same square‑free part.

        The problem reduces to grouping numbers by their square‑free part and
        taking the maximum total sum among the groups.
        """
        # Pre‑compute primes up to sqrt(max(nums)) using sieve. The constraint
        # on nums[i] is up to 1e9, sqrt is ~31623. Use a safe bound like 100000.
        limit = 100000
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        primes = []
        for i in range(2, limit + 1):
            if sieve[i]:
                primes.append(i)
                if i * i <= limit:
                    step = i
                    start = i * i
                    sieve[start:limit + 1:step] = [False] * ((limit - start) // step + 1)

        def square_free_part(x: int) -> int:
            """Return the square‑free part of x (product of primes with odd exponent)."""
            sf = 1
            temp = x
            for p in primes:
                if p * p > temp:
                    break
                cnt = 0
                while temp % p == 0:
                    temp //= p
                    cnt ^= 1  # parity of exponent
                if cnt:
                    sf *= p
            if temp > 1:
                # remaining prime factor appears once (odd exponent)
                sf *= temp
            return sf

        group_sum = {}
        max_sum = 0
        for v in nums:
            key = square_free_part(v)
            group_sum[key] = group_sum.get(key, 0) + v
            if group_sum[key] > max_sum:
                max_sum = group_sum[key]
        return max_sum
