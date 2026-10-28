from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player after 2^j passes from i; sm[j][i]: sum of the ids
        # of the 2^j players receiving the ball starting from i (excluding i).
        nxt = [list(receiver)]
        sm = [list(receiver)]
        j = 0
        while (1 << (j + 1)) <= k:
            pn = nxt[j]
            ps = sm[j]
            nn = [pn[pn[i]] for i in range(n)]
            ns = [ps[i] + ps[pn[i]] for i in range(n)]
            nxt.append(nn)
            sm.append(ns)
            j += 1
        best = 0
        for x in range(n):
            total = x
            cur = x
            kk = k
            b = 0
            while kk:
                if kk & 1:
                    total += sm[b][cur]
                    cur = nxt[b][cur]
                kk >>= 1
                b += 1
            if total > best:
                best = total
        return best
