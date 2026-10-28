from typing import *


class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        h = (n + 1) // 2
        full = (1 << k) - 1

        def rot(mask, s):
            s %= k
            return ((mask << s) | (mask >> (k - s))) & full if s else mask

        # trans[mask][w]: residues reachable from mask by adding d*w for any digit d in 0..9
        trans = [[0] * k for _ in range(full + 1)]
        for mask in range(full + 1):
            for w in range(k):
                res = 0
                for d in range(10):
                    res |= rot(mask, d * w)
                trans[mask][w] = res

        # weights
        pw = [1 % k] * n
        for i in range(1, n):
            pw[i] = pw[i - 1] * 10 % k
        w = [0] * h
        for i in range(h):
            j = n - 1 - i
            if i == j:
                w[i] = pw[i]
            else:
                w[i] = (pw[i] + pw[j]) % k

        # R[j]: residues that positions j..h-1 can sum to, such that the total ends at 0
        # We store "need" sets: R[j] = set of residues r such that the suffix from j
        # contributes r (so that prefix residue + r == 0 mod k is needed).
        # Simpler: track sets of suffix sums directly.
        R = [0] * (h + 1)
        R[h] = 1  # only sum 0
        for j in range(h - 1, -1, -1):
            R[j] = trans[R[j + 1]][w[j]]

        # Greedy from the front: need prefix residue cur such that cur + suffix == 0 mod k.
        # Condition: (cur + d*w[i]) must be such that the remaining suffix sum s satisfies
        # (new_cur + s) % k == 0 for some s in R[i+1]; i.e. -new_cur mod k in R[i+1].
        half = []
        cur = 0
        for i in range(h):
            lo = 1 if i == 0 else 0
            chosen = -1
            for d in range(9, lo - 1, -1):
                nc = (cur + d * w[i]) % k
                need = (-nc) % k
                if R[i + 1] >> need & 1:
                    chosen = d
                    cur = nc
                    break
            if chosen < 0:
                return ""
            half.append(str(chosen))

        first = "".join(half)
        if n % 2 == 1:
            return first + first[:-1][::-1]
        return first + first[::-1]
