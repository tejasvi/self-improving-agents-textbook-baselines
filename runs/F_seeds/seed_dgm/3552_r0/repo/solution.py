class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # p[j] = 10^j mod k
        p = [1 % k] * n
        for j in range(1, n):
            p[j] = p[j - 1] * 10 % k

        # w[i] = contribution mod k of digit at half-position i (mirrored pair)
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(p[i])
            else:
                w.append((p[i] + p[j]) % k)

        # R[i][r]: can positions i..h-1 be filled so the sum of contributions
        # is congruent to r (mod k) -- we store needed remainder to reach 0.
        # ok[i] is a list of booleans over remainders cur (sum so far before i)
        ok = [None] * (h + 1)
        ok[h] = [False] * k
        ok[h][0] = True
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            nxt = ok[i + 1]
            wi = w[i]
            cur = [False] * k
            for r in range(k):
                for d in range(9, lo - 1, -1):
                    if nxt[(r + d * wi) % k]:
                        cur[r] = True
                        break
            ok[i] = cur

        if not ok[0][0]:
            return ""

        digits = [0] * h
        r = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            wi = w[i]
            nxt = ok[i + 1]
            for d in range(9, lo - 1, -1):
                if nxt[(r + d * wi) % k]:
                    digits[i] = d
                    r = (r + d * wi) % k
                    break

        half = [str(d) for d in digits]
        s = half + [str(digits[i]) for i in range(h - 1 - (n % 2 == 1), -1, -1)]
        return "".join(s)
