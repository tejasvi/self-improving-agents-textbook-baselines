class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        m = len(s)
        S = int(s)
        base = 10 ** m

        def count_allowed_below(Q: int) -> int:
            # number of integers in [0, Q) whose digits are all <= limit
            if Q <= 0:
                return 0
            d = str(Q)
            L = len(d)
            k = limit + 1
            total = 0
            for i, ch in enumerate(d):
                c = int(ch)
                smaller = min(c, k)  # allowed digits strictly less than c
                total += smaller * k ** (L - i - 1)
                if c > limit:
                    return total
            return total

        def count(N: int) -> int:
            if N < S:
                return 0
            P = (N - S) // base
            return count_allowed_below(P + 1)

        return count(finish) - count(start - 1)
