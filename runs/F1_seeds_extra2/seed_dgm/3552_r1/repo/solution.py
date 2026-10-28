class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # p[j] = 10^j mod k
        p = [0] * n
        p[0] = 1 % k
        for j in range(1, n):
            p[j] = (p[j - 1] * 10) % k
        # weight of the digit at half-position i
        w = [0] * h
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w[i] = p[i]
            else:
                w[i] = (p[i] + p[j]) % k
        # suffix[i][r] : positions i..h-1 can contribute remainder r
        suffix = [None] * (h + 1)
        base = [False] * k
        base[0] = True
        suffix[h] = base
        for i in range(h - 1, -1, -1):
            nxt = suffix[i + 1]
            cur = [False] * k
            lo = 1 if i == 0 else 0
            wi = w[i]
            for d in range(lo, 10):
                dw = (d * wi) % k
                for r in range(k):
                    if nxt[r]:
                        cur[(dw + r) % k] = True
            suffix[i] = cur
        digits = []
        rem = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            nxt = suffix[i + 1]
            chosen = None
            for d in range(9, lo - 1, -1):
                t = (rem + d * w[i]) % k
                need = (-t) % k
                if nxt[need]:
                    chosen = d
                    rem = t
                    break
            if chosen is None:
                return ""
            digits.append(chosen)
        first = "".join(str(d) for d in digits)
        # build palindrome
        if n % 2 == 0:
            second = first[::-1]
        else:
            second = first[:-1][::-1]
        return first + second
