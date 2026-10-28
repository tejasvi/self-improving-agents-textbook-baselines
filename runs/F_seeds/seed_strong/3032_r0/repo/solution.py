from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player after 2^j passes from i
        # sm[j][i]: sum of ids of the 2^j players receiving the ball starting at i
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
        rem_bits = []
        b = 0
        while (1 << b) <= k:
            if (k >> b) & 1:
                rem_bits.append(b)
            b += 1
        for x in range(n):
            cur = x
            total = x
            for b in rem_bits:
                total += sm[b][cur]
                cur = nxt[b][cur]
            if total > best:
                best = total
        return best
