from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        nxt = list(receiver)
        sm = list(receiver)  # sum of receiver ids over 2^j passes starting at i
        cur_nxt = nxt
        cur_sm = sm
        kk = k
        # Position arrays for each start: pos[x] current node, tot[x] accumulated sum
        pos = list(range(n))
        tot = list(range(n))
        while kk:
            if kk & 1:
                for x in range(n):
                    p = pos[x]
                    tot[x] += cur_sm[p]
                    pos[x] = cur_nxt[p]
            kk >>= 1
            if kk:
                new_sm = [cur_sm[i] + cur_sm[cur_nxt[i]] for i in range(n)]
                new_nxt = [cur_nxt[cur_nxt[i]] for i in range(n)]
                cur_sm, cur_nxt = new_sm, new_nxt
        return max(tot)
