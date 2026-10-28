from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        # prefix digit-sum counts modulo 3 and 9 over prefixes S[0..i]
        cnt3 = [0] * 3
        cnt9 = [0] * 9
        cnt3[0] = 1
        cnt9[0] = 1
        S = 0  # digit sum of prefix (mod 9 is enough)
        # mod 7 DP: cnt7[r] = number of starts j<=i with value(j..i) % 7 == r
        cnt7 = [0] * 7
        for i in range(n):
            c = ord(s[i]) - 48
            # --- mod 7 update (value of s[j..i]) ---
            new7 = [0] * 7
            for r in range(7):
                if cnt7[r]:
                    new7[(10 * r + c) % 7] += cnt7[r]
            new7[c % 7] += 1
            cnt7 = new7
            # --- prefix digit sums ---
            S = (S + c) % 9
            if c == 0:
                cnt3[S % 3] += 1
                cnt9[S] += 1
                continue
            if c in (1, 2, 5):
                ans += i + 1
            elif c == 3:
                ans += cnt3[S % 3]
            elif c == 6:
                ans += cnt3[S % 3]
            elif c == 9:
                ans += cnt9[S]
            elif c == 7:
                ans += cnt7[0]
            elif c == 4:
                # value mod 4 depends on last two digits (for length >= 2)
                ans += 1  # length 1
                if i >= 1:
                    v2 = (ord(s[i - 1]) - 48) * 10 + c
                    ok = v2 % 4 == 0
                    # lengths 2..i+1
                    if ok:
                        ans += i
            elif c == 8:
                # value mod 8 depends on last three digits (for length >= 3)
                ans += 1  # length 1
                if i >= 1:
                    v2 = (ord(s[i - 1]) - 48) * 10 + c
                    if v2 % 8 == 0:
                        ans += 1  # length 2
                if i >= 2:
                    v3 = ((ord(s[i - 2]) - 48) * 100
                          + (ord(s[i - 1]) - 48) * 10 + c)
                    if v3 % 8 == 0:
                        ans += i - 1  # lengths 3..i+1
            cnt3[S % 3] += 1
            cnt9[S] += 1
        return ans
