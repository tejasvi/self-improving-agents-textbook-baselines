class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        # powers of 10 modulo k
        pw = [0] * n
        pw[0] = 1 % k
        for j in range(1, n):
            pw[j] = pw[j - 1] * 10 % k
        # weight of the digit at half-position i
        w = []
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w.append(pw[i])
            else:
                w.append((pw[i] + pw[j]) % k)
        # reach[i] = bitmask of residues achievable by positions i..h-1
        full = (1 << k) - 1
        reach = [0] * (h + 1)
        reach[h] = 1  # residue 0 only
        for i in range(h - 1, -1, -1):
            lo = 1 if i == 0 else 0
            nxt = reach[i + 1]
            mask = 0
            for d in range(lo, 10):
                shift = d * w[i] % k
                for r in range(k):
                    if nxt >> r & 1:
                        mask |= 1 << ((r + shift) % k)
            reach[i] = mask
        if not (reach[0] >> 0 & 1):
            return ""
        # greedy construction from the front
        t = 0
        half = []
        for i in range(h):
            lo = 1 if i == 0 else 0
            for d in range(9, lo - 1, -1):
                nt = (t - d * w[i]) % k
                if reach[i + 1] >> nt & 1:
                    half.append(d)
                    t = nt
                    break
        s = [str(d) for d in half]
        # build full palindrome
        rest = s[: n // 2]
        rest.reverse()
        return "".join(s) + "".join(rest)
