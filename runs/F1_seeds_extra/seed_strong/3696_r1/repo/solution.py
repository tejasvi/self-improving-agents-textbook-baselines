from typing import *


class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dig = [ord(ch) - 48 for ch in s]
        # V[d][j] = value of s[0:j] mod d
        V = [None] * 10
        for d in range(1, 10):
            arr = [0] * (n + 1)
            r = 0
            for j in range(n):
                r = (r * 10 + dig[j]) % d
                arr[j + 1] = r
            V[d] = arr

        # sols[d][p][r] = list of v in [0,d) with v*p % d == r
        sols = [None] * 10
        for d in range(1, 10):
            tab = [[[] for _ in range(d)] for _ in range(d)]
            for p in range(d):
                for v in range(d):
                    tab[p][(v * p) % d].append(v)
            sols[d] = tab

        # cnt[d][c][v]: number of prefix lengths j (j <= e-3) with j%6==c and V[d][j]==v
        cnt = [None] * 10
        for d in range(1, 10):
            cnt[d] = [[0] * d for _ in range(6)]

        ans = 0
        for e in range(1, n + 1):
            j = e - 3
            if j >= 0:
                cj = j % 6
                for d in range(1, 10):
                    cnt[d][cj][V[d][j]] += 1
            last = dig[e - 1]
            if last == 0:
                continue
            d = last
            ve = V[d][e]
            # short lengths 1 and 2
            if int(s[e - 1:e]) % d == 0:
                ans += 1
            if e >= 2 and int(s[e - 2:e]) % d == 0:
                ans += 1
            # lengths >= 3: j <= e-3
            if e >= 3:
                cd = cnt[d]
                for c in range(6):
                    # L = e - j, L ≡ (e - c) mod 6, pick representative in [3,8]
                    L = 3 + ((e - c - 3) % 6)
                    p = pow(10, L, d)
                    for v in sols[d][p][ve]:
                        ans += cd[c][v]
        return ans
