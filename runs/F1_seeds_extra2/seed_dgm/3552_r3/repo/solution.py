class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # weight of half-digit at index i, modulo k
        w = [0] * h
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w[i] = pow(10, i, k) % k
            else:
                w[i] = (pow(10, i, k) + pow(10, j, k)) % k

        # feasible[i][r]: positions i..h-1 can sum to remainder r (mod k)
        feasible = [None] * (h + 1)
        last = [False] * k
        last[0] = True
        feasible[h] = last
        for i in range(h - 1, -1, -1):
            nxt = feasible[i + 1]
            cur = [False] * k
            lo = 1 if i == 0 else 0
            wi = w[i]
            for d in range(lo, 10):
                dw = (d * wi) % k
                for r in range(k):
                    if not cur[r] and nxt[(r - dw) % k]:
                        cur[r] = True
            feasible[i] = cur

        if not feasible[0][0]:
            return ""

        half = []
        rem = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            nxt = feasible[i + 1]
            for d in range(9, lo - 1, -1):
                nr = (rem - d * w[i]) % k
                if nxt[nr]:
                    half.append(d)
                    rem = nr
                    break

        digits = [str(half[min(i, n - 1 - i)]) for i in range(n)]
        return "".join(digits)
