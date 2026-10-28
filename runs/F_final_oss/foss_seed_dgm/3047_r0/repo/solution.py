from typing import List

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        """Return the maximum element-sum of a complete subset.

        Two numbers a and b have product a*b that is a perfect square iff the
        parity (odd/even) of the exponent of every prime factor is the same for
        a and b.  Consequently, every element in a complete subset must share the
        same *square‑free kernel* – the product of primes that appear with odd
        exponent in its prime factorisation.

        The optimal subset for a particular kernel is simply all numbers that
        share this kernel, because adding more elements never breaks the
        condition.  Hence the answer is the maximum sum of numbers grouped by
        their kernel.
        """
        if not nums:
            return 0

        # Generate primes up to sqrt(max(nums)).
        import math
        max_num = max(nums)
        limit = int(math.isqrt(max_num)) + 1
        sieve = [True] * (limit + 1)
        primes = []
        for i in range(2, limit + 1):
            if sieve[i]:
                primes.append(i)
                step = i
                start = i * i
                if start <= limit:
                    for j in range(start, limit + 1, step):
                        sieve[j] = False

        def square_free(x: int) -> int:
            """Return the product of primes that have odd exponent in x.

            This is also known as the square‑free kernel of x.
            """
            res = 1
            tmp = x
            for p in primes:
                if p * p > tmp:
                    break
                cnt = 0
                while tmp % p == 0:
                    tmp //= p
                    cnt ^= 1  # toggle parity
                if cnt:
                    res *= p
            # Remaining factor is prime with exponent 1 (odd) if >1.
            if tmp > 1:
                res *= tmp
            return res

        # Group sums by kernel.
        from collections import defaultdict
        group_sum = defaultdict(int)
        for v in nums:
            key = square_free(v)
            group_sum[key] += v

        # The maximum sum among groups (singletons are naturally included).
        return max(group_sum.values())
