from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # cnt4/cnt7/cnt8: residues of value(s[j..i]) mod d over start j <= i
        cnt = {4: [0] * 4, 7: [0] * 7, 8: [0] * 8}
        # prefix digit sums residues mod 3 and mod 9 over j in [0..i]
        c3 = [0] * 3
        c9 = [0] * 9
        c3[0] = 1
        c9[0] = 1
        P = 0  # digit sum of prefix, not reduced
        ans = 0
        for i in range(n):
            c = ord(s[i]) - 48
            # update residue arrays for all d in {4,7,8} with new digit c
            for d, arr in cnt.items():
                new = [0] * d
                for r in range(d):
                    v = arr[r]
                    if v:
                        new[(10 * r + c) % d] += v
                new[c % d] += 1
                cnt[d] = new
            P += c
            if c == 0:
                # substring ends in 0: not allowed; still update prefix counts
                c3[P % 3] += 1
                c9[P % 9] += 1
                continue
            if c == 1 or c == 2 or c == 5:
                ans += i + 1
            elif c == 3 or c == 6:
                ans += c3[P % 3]
            elif c == 9:
                ans += c9[P % 9]
            else:  # 4, 7, 8
                ans += cnt[c][0]
            c3[P % 3] += 1
            c9[P % 9] += 1
        return ans
