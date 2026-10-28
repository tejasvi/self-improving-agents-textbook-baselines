from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        LOG = max(1, k.bit_length())
        # nxt[j][i]: player after 2^j passes from i
        # sm[j][i]: sum of ids received during the 2^j passes starting at i
        nxt = [list(receiver)]
        sm = [list(receiver)]
        for j in range(1, LOG):
            pn = nxt[j - 1]
            ps = sm[j - 1]
            nn = [pn[pn[i]] for i in range(n)]
            ns = [ps[i] + ps[pn[i]] for i in range(n)]
            nxt.append(nn)
            sm.append(ns)
        best = 0
        for i in range(n):
            cur = i
            total = i
            rem = k
            j = 0
            while rem:
                if rem & 1:
                    total += sm[j][cur]
                    cur = nxt[j][cur]
                rem >>= 1
                j += 1
            if total > best:
                best = total
        return best
