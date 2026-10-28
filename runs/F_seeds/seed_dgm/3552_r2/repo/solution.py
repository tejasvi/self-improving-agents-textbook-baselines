class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # p[j] = 10^j mod k
        p = [1 % k] * n
        for j in range(1, n):
            p[j] = p[j - 1] * 10 % k
        # w[i]: contribution (mod k) of digit at half-position i per unit digit
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(p[i])
            else:
                w.append((p[i] + p[j]) % k)
        # S[i][r]: can positions i..h-1 sum to remainder r (mod k)
        S = [None] * (h + 1)
        S[h] = [False] * k
        S[h][0] = True
        for i in range(h - 1, -1, -1):
            nxt = S[i + 1]
            cur = [False] * k
            wi = w[i]
            for d in range(10):
                shift = d * wi % k
                for r in range(k):
                    if nxt[r]:
                        cur[(r + shift) % k] = True
            S[i] = cur
        if not S[0][0]:
            return ""
        digits = []
        rem = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                nr = (rem + d * w[i]) % k
                need = (-nr) % k
                if S[i + 1][need]:
                    chosen = d
                    rem = nr
                    break
            if chosen is None:
                return ""
            digits.append(chosen)
        s = [0] * n
        for i in range(h):
            s[i] = digits[i]
            s[n - 1 - i] = digits[i]
        return "".join(str(c) for c in s)
