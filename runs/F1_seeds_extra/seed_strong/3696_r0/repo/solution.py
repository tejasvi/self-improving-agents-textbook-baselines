from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        digits = [ord(c) - 48 for c in s]

        # Prefix counts for digit-sum residues mod 3 and mod 9 (for d=3,6,9),
        # and for the key P[k]*10^{-k} mod 7 (for d=7).
        cnt3 = [0, 0, 0]
        cnt9 = [0] * 9
        cnt7 = [0] * 7
        S3 = 0          # digit sum mod 3 of prefix
        S9 = 0          # digit sum mod 9 of prefix
        P7 = 0          # value of prefix mod 7
        inv10pow = 1    # 10^{-k} mod 7 (inverse of 10 is 5 mod 7)
        cnt3[0] += 1
        cnt9[0] += 1
        cnt7[0] += 1    # key for k=0: P=0 -> 0

        total = 0
        for i in range(n):
            d = digits[i]
            # Advance prefix to i+1
            S3 = (S3 + d) % 3
            S9 = (S9 + d) % 9
            P7 = (P7 * 10 + d) % 7
            inv10pow = (inv10pow * 5) % 7   # 10^{-(i+1)} mod 7
            key7 = (P7 * inv10pow) % 7

            if d == 0:
                # Keep counts updated, but no query.
                pass
            elif d in (1, 2, 5):
                total += i + 1
            elif d == 3:
                total += cnt3[S3]
            elif d == 9:
                total += cnt9[S9]
            elif d == 6:
                total += cnt3[S3]
            elif d == 7:
                total += cnt7[key7]
            elif d in (4, 8):
                t = 2 if d == 4 else 3
                # Substrings of length >= t: divisibility fixed by last t digits.
                if i - t + 1 >= 0:
                    v = 0
                    for k in range(i - t + 1, i + 1):
                        v = v * 10 + digits[k]
                    if v % d == 0:
                        total += i - t + 2
                # Substrings of length < t: check directly.
                for j in range(max(0, i - t + 2), i + 1):
                    v = 0
                    for k in range(j, i + 1):
                        v = v * 10 + digits[k]
                    if v % d == 0:
                        total += 1

            # Add prefix i+1 to the counts (for future queries).
            cnt3[S3] += 1
            cnt9[S9] += 1
            cnt7[P7 * inv10pow % 7] += 1

        return total
