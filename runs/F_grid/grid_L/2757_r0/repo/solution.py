class Solution:
    MOD = 10**9 + 7
    MAXL = 25
    MAXS = 9 * MAXL

    def __init__(self):
        # ways[l][s] = number of digit strings of length l with digit sum s
        ways = [[0] * (self.MAXS + 1) for _ in range(self.MAXL + 1)]
        ways[0][0] = 1
        for l in range(1, self.MAXL + 1):
            prev, cur = ways[l - 1], ways[l]
            for s in range(self.MAXS + 1):
                if prev[s]:
                    for d in range(10):
                        if s + d <= self.MAXS:
                            cur[s + d] += prev[s]
        # pre[l][s] = sum of ways[l][0..s-1]
        self.pre = []
        for l in range(self.MAXL + 1):
            p = [0] * (self.MAXS + 2)
            for s in range(self.MAXS + 1):
                p[s + 1] = p[s] + ways[l][s]
            self.pre.append(p)

    def _range_count(self, l: int, lo: int, hi: int) -> int:
        # number of strings of length l with digit sum in [lo, hi]
        lo = max(lo, 0)
        hi = min(hi, self.MAXS)
        if lo > hi:
            return 0
        return self.pre[l][hi + 1] - self.pre[l][lo]

    def _upto(self, n: str, lo: int, hi: int) -> int:
        # count integers x in [0, int(n)] with digit sum in [lo, hi]
        L = len(n)
        total = 0
        prefix = 0
        for i, ch in enumerate(n):
            c = int(ch)
            rem = L - i - 1
            for d in range(c):
                total += self._range_count(rem, lo - prefix - d, hi - prefix - d)
            prefix += c
        if lo <= prefix <= hi:
            total += 1
        return total

    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        res = self._upto(num2, min_sum, max_sum) - self._upto(num1, min_sum, max_sum)
        if min_sum <= sum(int(c) for c in num1) <= max_sum:
            res += 1
        return res % self.MOD
