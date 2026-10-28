class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        if k == 1:
            return "9" * n
        h = (n + 1) // 2
        # weight of digit at half-index i (mod k)
        pw = [1] * n
        for i in range(1, n):
            pw[i] = pw[i - 1] * 10 % k
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(pw[i] % k)
            else:
                w.append((pw[i] + pw[j]) % k)

        # can[i]: bitmask of residues reachable by positions i..h-1
        full = (1 << k) - 1

        def rot(mask, s):
            s %= k
            if s == 0:
                return mask
            return ((mask << s) | (mask >> (k - s))) & full

        can = [0] * (h + 1)
        can[h] = 1  # residue 0
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            m = 0
            for d in range(lo, 10):
                m |= rot(can[i + 1], d * w[i])
            can[i] = m

        res = []
        p = 0  # residue of chosen prefix
        for i in range(h):
            lo = 1 if i == 0 else 0
            chosen = None
            for d in range(9, lo - 1, -1):
                s = (p + d * w[i]) % k
                need = (-s) % k
                if (can[i + 1] >> need) & 1:
                    chosen = d
                    p = s
                    break
            res.append(chosen)
        half = res
        if n % 2 == 0:
            full_digits = half + half[::-1]
        else:
            full_digits = half + half[-2::-1]
        return "".join(map(str, full_digits))
