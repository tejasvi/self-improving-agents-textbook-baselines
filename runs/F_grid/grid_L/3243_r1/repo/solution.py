class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        S = int(s)
        L = len(s)
        base = 10 ** L

        def count_upto(M: int) -> int:
            # count integers p in [0, M] whose digits are all <= limit
            if M < 0:
                return 0
            digits = str(M)
            n = len(digits)
            total = 0
            k = limit + 1
            for i, ch in enumerate(digits):
                c = int(ch)
                rem = n - i - 1
                # digits strictly less than c that are allowed
                total += min(k, c) * (k ** rem)
                if c > limit:
                    return total
            return total + 1  # M itself is valid

        def f(N: int) -> int:
            if N < S:
                return 0
            M = (N - S) // base
            return count_upto(M)

        return f(finish) - f(start - 1)
