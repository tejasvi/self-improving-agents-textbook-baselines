class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # Weight of half-digit i (digit at positions i and n-1-i) modulo k.
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(pow(10, i, k))
            else:
                w.append((pow(10, i, k) + pow(10, j, k)) % k)

        full = (1 << k) - 1

        def shift(mask, s):
            s %= k
            m = ((mask << s) | (mask >> (k - s))) & full if s else mask
            return m

        # can[i]: bitmask of residues achievable by digits at half-positions i..h-1
        can = [0] * (h + 1)
        can[h] = 1  # residue 0 only
        for i in range(h - 1, -1, -1):
            m = 0
            lo = 1 if i == 0 else 0
            for d in range(lo, 10):
                m |= shift(can[i + 1], d * w[i])
            can[i] = m

        if not (can[0] & 1):
            return ""

        # Greedy construction: need suffix residue `cur` to be fulfilled.
        cur = 0
        digits = []
        for i in range(h):
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                nxt = (cur - d * w[i]) % k
                if (can[i + 1] >> nxt) & 1:
                    chosen = d
                    cur = nxt
                    break
            digits.append(chosen)

        half = digits
        if n % 2 == 0:
            full_digits = half + half[::-1]
        else:
            full_digits = half + half[-2::-1]
        return "".join(map(str, full_digits))
