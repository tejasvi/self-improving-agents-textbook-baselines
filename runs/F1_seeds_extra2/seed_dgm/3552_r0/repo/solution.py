class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # weight of digit at half-position i in the total value mod k
        weights = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w = pow(10, i, k)
            else:
                w = (pow(10, i, k) + pow(10, j, k)) % k
            weights.append(w)

        def digits_for(i):
            return range(9, 0, -1) if i == 0 else range(9, -1, -1)

        # reach[i][r]: positions i..h-1 can be filled to sum to remainder r
        reach = [None] * (h + 1)
        reach[h] = [False] * k
        reach[h][0] = True
        for i in range(h - 1, -1, -1):
            cur = [False] * k
            nxt = reach[i + 1]
            w = weights[i]
            ds = range(1, 10) if i == 0 else range(10)
            for d in ds:
                add = (d * w) % k
                for r in range(k):
                    if nxt[r]:
                        cur[(r + add) % k] = True
            reach[i] = cur

        if not reach[0][0]:
            # no k-palindrome with n digits exists (should not happen for n>=1 since
            # we can always search; kept as a safety fallback)
            return ""

        half = []
        rem = 0
        for i in range(h):
            w = weights[i]
            chosen = None
            for d in digits_for(i):
                nr = (rem + d * w) % k
                # need remaining positions to produce (-nr) mod k
                if reach[i + 1][(-nr) % k]:
                    chosen = d
                    rem = nr
                    break
            half.append(chosen)

        s = [str(d) for d in half]
        # full palindrome: mirror of first n//2 digits, middle digit kept if odd
        if n % 2 == 0:
            tail = s[::-1]
        else:
            tail = s[:-1][::-1]
        return "".join(s + tail)
