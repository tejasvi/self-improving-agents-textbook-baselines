import numpy as np


class Solution:
    def countSubstrings(self, s: str) -> int:
        M = 2520  # lcm(1..9)
        # dp[r] = number of start positions j such that value(s[j..i]) % M == r
        dp = np.zeros(M, dtype=np.int64)
        # For residue r = q*252 + t (q in 0..9), image under r -> 10r + c mod M
        # depends only on t, and t -> (10t + c) % M is injective on 0..251.
        t_idx = np.arange(252, dtype=np.int64) * 10
        # Precompute image indices for each digit c
        imgs = [(t_idx + c) % M for c in range(10)]
        # Residues divisible by c (since c | M)
        total = 0
        for ch in s:
            c = ord(ch) - 48
            S = dp.reshape(10, 252).sum(axis=0)
            new = np.zeros(M, dtype=np.int64)
            new[imgs[c]] = S
            new[c] += 1  # substring starting at current position
            dp = new
            if c:
                total += int(dp[::c].sum())
        return total
