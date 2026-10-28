from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dig = [ord(c) - 48 for c in s]
        # S[k]: digit sum of s[0..k-1]; prefix keys for mod 3 and mod 9
        S = [0] * (n + 1)
        # Q[k] = (value of s[0..k-1]) * 5^k mod 7
        Q = [0] * (n + 1)
        P = 0
        pw = 1
        for k in range(n):
            S[k + 1] = S[k] + dig[k]
            P = (P * 10 + dig[k]) % 7
            pw = pw * 5 % 7  # 5^(k+1)
            Q[k + 1] = P * pw % 7
        cnt3 = [0] * 3
        cnt9 = [0] * 9
        cnt7 = [0] * 7
        cnt3[0] += 1
        cnt9[0] += 1
        cnt7[0] += 1  # prefix index 0: Q[0] = 0
        total = 0
        for j in range(n):
            d = dig[j]
            if d != 0:
                if d == 1 or d == 2 or d == 5:
                    total += j + 1
                elif d == 3 or d == 6:
                    total += cnt3[S[j + 1] % 3]
                elif d == 9:
                    total += cnt9[S[j + 1] % 9]
                elif d == 7:
                    total += cnt7[Q[j + 1]]
                elif d == 4 or d == 8:
                    for L in range(1, min(3, j + 1) + 1):
                        if int(s[j - L + 1:j + 1]) % d == 0:
                            total += 1
                    if j + 1 > 3 and int(s[j - 2:j + 1]) % d == 0:
                        total += j + 1 - 3
            # register prefix index j+1 for future queries
            cnt3[S[j + 1] % 3] += 1
            cnt9[S[j + 1] % 9] += 1
            cnt7[Q[j + 1]] += 1
        return total
