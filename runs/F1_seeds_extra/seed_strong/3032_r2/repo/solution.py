from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: position after 2^j passes from i; sm[i]: sum of ids received in those passes
        nxt = list(receiver)
        sm = list(receiver)
        pos = list(range(n))
        total = list(range(n))  # x + sum so far
        kk = k
        while kk:
            if kk & 1:
                for x in range(n):
                    p = pos[x]
                    total[x] += sm[p]
                    pos[x] = nxt[p]
            kk >>= 1
            if kk:
                nsm = [sm[i] + sm[nxt[i]] for i in range(n)]
                nnxt = [nxt[nxt[i]] for i in range(n)]
                sm, nxt = nsm, nnxt
        return max(total)
