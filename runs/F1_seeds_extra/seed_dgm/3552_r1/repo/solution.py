class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        half = (n + 1) // 2

        # w[i]: contribution (mod k) of digit placed at pair i (both mirrored positions)
        w = [0] * half
        p = 1 % k  # 10^i mod k
        for i in range(half):
            j = n - 1 - i
            if i == j:
                w[i] = p % k
            else:
                pj = pow(10, j, k)
                w[i] = (p + pj) % k
            p = (p * 10) % k

        # reach[i][r]: can digits of pairs i..half-1 sum to remainder r (mod k)
        reach = [None] * (half + 1)
        base = [False] * k
        base[0] = True
        reach[half] = base
        for i in range(half - 1, -1, -1):
            nxt = reach[i + 1]
            cur = [False] * k
            lo = 1 if i == 0 else 0
            for d in range(lo, 10):
                shift = (d * w[i]) % k
                for r in range(k):
                    if nxt[r]:
                        cur[(r + shift) % k] = True
            reach[i] = cur

        digits = [0] * half
        need = 0  # remainder accumulated so far
        for i in range(half):
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                s = (need + d * w[i]) % k
                # need remaining sum r in reach[i+1] with (s + r) % k == 0
                if reach[i + 1][(-s) % k]:
                    chosen = d
                    need = s
                    break
            if chosen is None:
                return ""
            digits[i] = chosen

        left = digits
        if n % 2 == 1:
            right = left[-2::-1]
        else:
            right = left[::-1]
        return "".join(str(d) for d in left) + "".join(str(d) for d in right)
