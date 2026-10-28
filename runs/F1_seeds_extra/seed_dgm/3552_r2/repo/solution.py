class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        # weight of digit at left-half position i in the total value mod k
        weights = []
        for i in range(h):
            j = n - 1 - i  # mirrored position (power of 10)
            if i == j:
                w = pow(10, i, k)
            else:
                w = (pow(10, i, k) + pow(10, j, k)) % k
            weights.append(w)

        # reach[i] = bitmask of residues achievable by positions i..h-1
        reach = [0] * (h + 1)
        reach[h] = 1  # residue 0 only
        for i in range(h - 1, -1, -1):
            w = weights[i]
            contrib = [(d * w) % k for d in range(10)]
            prev = reach[i + 1]
            cur = 0
            for r in range(k):
                if prev >> r & 1:
                    for c in contrib:
                        cur |= 1 << ((r + c) % k)
            reach[i] = cur & full

        digits = []
        r = 0  # residue of fixed prefix
        for i in range(h):
            w = weights[i]
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                nr = (r + d * w) % k
                # need remaining positions to reach residue (-nr) mod k
                if reach[i + 1] >> ((-nr) % k) & 1:
                    chosen = d
                    r = nr
                    break
            if chosen is None:
                return ""  # should not happen for valid inputs
            digits.append(chosen)

        half = digits
        if n % 2 == 0:
            rest = half[::-1]
        else:
            rest = half[:-1][::-1]
        return "".join(map(str, half + rest))
