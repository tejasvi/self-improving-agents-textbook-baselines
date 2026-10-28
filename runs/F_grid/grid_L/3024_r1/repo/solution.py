class Solution:
    def numberOfWays(self, s: str, t: str, k: int) -> int:
        MOD = 10 ** 9 + 7
        n = len(s)

        # KMP: find all p in [0, n) such that t occurs at position p in s+s,
        # i.e. rotating s by p gives t.
        pi = [0] * n
        j = 0
        for i in range(1, n):
            while j and t[i] != t[j]:
                j = pi[j - 1]
            if t[i] == t[j]:
                j += 1
            pi[i] = j

        text = s + s[:-1]
        count = 0      # total valid rotations p in [0, n)
        zero_valid = False
        j = 0
        for i, ch in enumerate(text):
            while j and ch != t[j]:
                j = pi[j - 1]
            if ch == t[j]:
                j += 1
            if j == n:
                start = i - n + 1
                if start < n:
                    count += 1
                    if start == 0:
                        zero_valid = True
                j = pi[j - 1]

        if count == 0:
            return 0

        # Number of sequences of k elements from Z_n \ {0} summing to 0 / to d != 0.
        sign = 1 if k % 2 == 0 else MOD - 1
        base = (n - 1) % MOD
        pk = pow(base, k, MOD)
        inv_n = pow(n, MOD - 2, MOD)
        f0 = (pk + base * sign) % MOD * inv_n % MOD
        f1 = (pk - sign) % MOD * inv_n % MOD

        if zero_valid:
            return (f0 + (count - 1) * f1) % MOD
        return count * f1 % MOD
