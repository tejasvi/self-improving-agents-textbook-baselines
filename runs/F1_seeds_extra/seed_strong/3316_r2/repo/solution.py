from typing import *


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)
        D = sorted(set(a[j] - a[i] for i in range(n) for j in range(i + 1, n)))

        total = 0
        prev = 0
        for d in D:
            # ways[c][i]: number of ways to choose c elements ending at index i
            # with every adjacent gap >= d
            # lim[i]: largest index p with a[p] <= a[i] - d (or -1)
            lim = []
            p = -1
            for i in range(n):
                while p + 1 < n and a[p + 1] <= a[i] - d:
                    p += 1
                lim.append(p)
            # dp for c = 1
            cur = [1] * n
            for c in range(2, k + 1):
                # prefix sums of cur
                pref = [0] * (n + 1)
                for i in range(n):
                    pref[i + 1] = (pref[i] + cur[i]) % MOD
                nxt = [0] * n
                for i in range(n):
                    L = lim[i]
                    if L >= 0:
                        nxt[i] = pref[L + 1]
                cur = nxt
            cnt = sum(cur) % MOD
            total = (total + (d - prev) * cnt) % MOD
            prev = d
        return total % MOD
