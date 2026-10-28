from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        # For each divisor d in 1..9, cnt[d][r] = number of start positions i
        # such that value(s[i..j]) % d == r, for the current end j.
        cnt = {d: [0] * d for d in range(1, 10)}
        # trans[d][c][r] = (10*r + c) % d
        trans = {d: [[(10 * r + c) % d for r in range(d)] for c in range(10)]
                 for d in range(1, 10)}
        ans = 0
        for ch in s:
            c = ord(ch) - 48
            for d in range(1, 10):
                old = cnt[d]
                t = trans[d][c]
                new = [0] * d
                for r in range(d):
                    v = old[r]
                    if v:
                        new[t[r]] += v
                new[c % d] += 1
                cnt[d] = new
                if c == d:
                    ans += new[0]
        return ans
