MOD = 10**9 + 7


class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        maxlen = len(num2)
        maxs = max_sum
        # ways[L][s]: number of digit strings of length L with digit sum s (s <= maxs)
        ways = [[0] * (maxs + 1) for _ in range(maxlen + 1)]
        ways[0][0] = 1
        for L in range(1, maxlen + 1):
            prev = ways[L - 1]
            cur = ways[L]
            for s in range(maxs + 1):
                if prev[s]:
                    for d in range(10):
                        if s + d <= maxs:
                            cur[s + d] += prev[s]
        # cum[L][s] = sum_{t<=s} ways[L][t]
        cum = []
        for L in range(maxlen + 1):
            row = [0] * (maxs + 1)
            acc = 0
            for s in range(maxs + 1):
                acc += ways[L][s]
                row[s] = acc
            cum.append(row)

        def range_count(L, lo, hi):
            # number of strings of length L with digit sum in [lo, hi]
            lo = max(lo, 0)
            hi = min(hi, maxs)
            if lo > hi:
                return 0
            return cum[L][hi] - (cum[L][lo - 1] if lo > 0 else 0)

        def f(X: str) -> int:
            # count integers x in [0, X] with min_sum <= digitsum(x) <= max_sum
            n = len(X)
            total = 0
            prefix = 0
            for i, ch in enumerate(X):
                c = int(ch)
                L = n - i - 1
                for d in range(c):
                    total += range_count(L, min_sum - prefix - d, max_sum - prefix - d)
                prefix += c
                if prefix > max_sum:
                    break
            else:
                if min_sum <= prefix <= max_sum:
                    total += 1
            return total % MOD

        good1 = 1 if min_sum <= sum(map(int, num1)) <= max_sum else 0
        return (f(num2) - f(num1) + good1) % MOD
