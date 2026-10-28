class Solution:
    MOD = 10 ** 9 + 7

    def countSteppingNumbers(self, low: str, high: str) -> int:
        MOD = self.MOD

        # ways[k][d]: number of digit sequences of length k that can follow digit d
        # such that every adjacent difference is exactly 1.
        maxlen = max(len(low), len(high)) + 1
        ways = [[0] * 10 for _ in range(maxlen + 1)]
        for d in range(10):
            ways[0][d] = 1
        for k in range(1, maxlen + 1):
            for d in range(10):
                total = 0
                if d - 1 >= 0:
                    total += ways[k - 1][d - 1]
                if d + 1 <= 9:
                    total += ways[k - 1][d + 1]
                ways[k][d] = total % MOD

        def count_upto(N: str) -> int:
            """Number of stepping numbers in [1, N] (N given as a digit string, no leading zeros)."""
            n = len(N)
            if n == 0:
                return 0
            res = 0
            # Shorter lengths L < n: first digit 1..9
            for L in range(1, n):
                for d in range(1, 10):
                    res += ways[L - 1][d]
            # Same length n, tight prefix walk
            prefix_ok = True
            for i in range(n):
                cur = ord(N[i]) - 48
                start = 1 if i == 0 else 0
                rem = n - i - 1
                for d in range(start, cur):
                    if i == 0 or abs(d - prev) == 1:
                        res += ways[rem][d]
                if i > 0 and abs(cur - prev) != 1:
                    prefix_ok = False
                    break
                prev = cur
            if prefix_ok:
                res += 1  # N itself is a stepping number
            return res % MOD

        def is_stepping(s: str) -> bool:
            for i in range(1, len(s)):
                if abs(ord(s[i]) - ord(s[i - 1])) != 1:
                    return False
            return True

        ans = count_upto(high) - count_upto(low) + (1 if is_stepping(low) else 0)
        return ans % MOD
