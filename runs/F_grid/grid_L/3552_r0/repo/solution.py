class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # weight of each free half-position i (0-indexed from most significant)
        weights = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w = pow(10, i, k)
            else:
                w = (pow(10, i, k) + pow(10, j, k)) % k
            weights.append(w)

        def digit_range(i):
            return range(1, 10) if i == 0 else range(0, 10)

        # feasible[i][r]: suffix positions i..h-1 can sum to residue r
        feasible = [None] * (h + 1)
        base = [False] * k
        base[0] = True
        feasible[h] = base
        for i in range(h - 1, -1, -1):
            w = weights[i]
            nxt = feasible[i + 1]
            cur = [False] * k
            for d in digit_range(i):
                dw = (d * w) % k
                for r in range(k):
                    if nxt[r]:
                        cur[(r + dw) % k] = True
            feasible[i] = cur

        if not feasible[0][0]:
            return ""

        digits = [0] * h
        r = 0  # residue still needed from positions i..h-1
        for i in range(h):
            w = weights[i]
            nxt = feasible[i + 1]
            for d in reversed(digit_range(i)):
                need = (r - d * w) % k
                if nxt[need]:
                    digits[i] = d
                    r = need
                    break

        half = digits
        s = [str(d) for d in half]
        # mirror: full = half + reversed(half without middle if n odd)
        if n % 2 == 1:
            rest = s[:-1]
        else:
            rest = s
        return "".join(s) + "".join(reversed(rest))
