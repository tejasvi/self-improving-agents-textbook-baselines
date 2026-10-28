from typing import *


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Values are < 128, so OR results are < 128 too.
        # A set of OR values is stored as a 128-bit mask (bit v <=> value v).
        # T[x][p][b]: mask of {(8p+i)|x : bit i set in b}; used to map a set
        # through "v -> v|x" quickly, 16 byte-lookups per transition.
        cache = {}

        def table(x):
            if x in cache:
                return cache[x]
            tab = []
            for p in range(16):
                row = [0] * 256
                for b in range(1, 256):
                    low = b & -b
                    i = low.bit_length() - 1
                    row[b] = row[b ^ low] | (1 << ((8 * p + i) | x))
                tab.append(row)
            cache[x] = tab
            return tab

        def apply(mask, x):
            tab = table(x)
            res = 0
            p = 0
            while mask:
                byte = mask & 0xFF
                if byte:
                    res |= tab[p][byte]
                mask >>= 8
                p += 1
            return res

        def achievable(seq):
            # res[i] = mask of OR values from exactly k elements of seq[:i]
            f = [0] * (k + 1)
            f[0] = 1  # OR of empty set = 0
            res = [0] * (len(seq) + 1)
            for i, x in enumerate(seq):
                res[i] = f[k]
                for j in range(k, 0, -1):
                    if f[j - 1]:
                        f[j] |= apply(f[j - 1], x)
            res[len(seq)] = f[k]
            return res

        pre = achievable(nums)
        suf = achievable(nums[::-1])

        def bits(mask):
            out = []
            v = 0
            while mask:
                if mask & 1:
                    out.append(v)
                mask >>= 1
                v += 1
            return out

        best = 0
        for m in range(k, n - k + 1):
            P = pre[m]
            S = suf[n - m]
            if not P or not S:
                continue
            Sv = bits(S)
            # prefix sets of S at each bit level for greedy max-xor
            levels = [set(b >> bit for b in Sv) for bit in range(7)]
            for a in bits(P):
                cur = 0
                for bit in range(6, -1, -1):
                    t = 1 - ((a >> bit) & 1)
                    cand = (cur << 1) | t
                    if cand in levels[bit]:
                        cur = cand
                    else:
                        cur = (cur << 1) | (1 - t)
                val = a ^ cur
                if val > best:
                    best = val
        return best
