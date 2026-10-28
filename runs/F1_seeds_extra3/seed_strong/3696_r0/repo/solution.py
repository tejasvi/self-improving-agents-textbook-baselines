from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        # For each modulus d in 2..9, cnt[d][r] = number of start positions i
        # (i <= j) such that value(s[i..j]) % d == r, for the current end j.
        mods = range(2, 10)
        cnt = {d: [0] * d for d in mods}
        ans = 0
        for j, ch in enumerate(s):
            c = ord(ch) - 48
            for d in mods:
                old = cnt[d]
                new = [0] * d
                for r in range(d):
                    v = old[r]
                    if v:
                        new[(10 * r + c) % d] += v
                new[c % d] += 1  # substring starting at j
                cnt[d] = new
            if c == 1:
                ans += j + 1  # every substring is divisible by 1
            elif c >= 2:
                ans += cnt[c][0]  # residue 0 mod c; c != 0 so last digit nonzero
        return ans
