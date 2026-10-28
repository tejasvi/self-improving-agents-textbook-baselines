from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt: destination after 2^j passes; sm: sum of ids of the 2^j nodes
        # starting at i (i itself included, the final destination excluded).
        nxt = list(receiver)
        sm = list(range(n))
        best = 0
        # cur_total for each start x is computed by walking the bits of k.
        cur = list(range(n))
        tot = [0] * n
        kk = k
        while kk:
            if kk & 1:
                tot = [tot[i] + sm[cur[i]] for i in range(n)]
                cur = [nxt[cur[i]] for i in range(n)]
            kk >>= 1
            if kk:
                sm = [sm[i] + sm[nxt[i]] for i in range(n)]
                nxt = [nxt[nxt[i]] for i in range(n)]
        for x in range(n):
            v = tot[x] + cur[x]
            if v > best:
                best = v
        return best
