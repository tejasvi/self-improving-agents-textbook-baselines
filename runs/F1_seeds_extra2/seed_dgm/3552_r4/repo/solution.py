class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # pow10[p] = 10^p mod k
        pow10 = [0] * n
        pow10[0] = 1 % k
        for p in range(1, n):
            pow10[p] = pow10[p - 1] * 10 % k

        # weight of digit at half-position i (contributes to both mirrored places)
        def weight(i):
            j = n - 1 - i
            if i == j:
                return pow10[i]
            return (pow10[i] + pow10[j]) % k

        w = [weight(i) for i in range(h)]

        # reach[i][r]: positions i..h-1 can sum to residue r (mod k)
        reach = [None] * (h + 1)
        last = [False] * k
        last[0] = True
        reach[h] = last
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            cur = [False] * k
            nxt = reach[i + 1]
            wi = w[i]
            for d in range(lo, 10):
                dw = d * wi % k
                for r in range(k):
                    if nxt[r]:
                        cur[(r + dw) % k] = True
            reach[i] = cur

        digits = [0] * h
        total = 0  # residue of chosen prefix
        for i in range(h):
            lo = 1 if i == 0 else 0
            nxt = reach[i + 1]
            wi = w[i]
            chosen = None
            for d in range(9, lo - 1, -1):
                s = (total + d * wi) % k
                if nxt[(-s) % k]:
                    chosen = d
                    total = s
                    break
            digits[i] = chosen

        half = [str(d) for d in digits]
        if n % 2 == 0:
            tail = half[::-1]
        else:
            tail = half[:-1][::-1]
        return "".join(half + tail)
