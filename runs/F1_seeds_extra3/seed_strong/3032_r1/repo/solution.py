from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: player after 2^j passes from i; sm[i]: sum of receivers
        # visited during those 2^j passes (excluding start, including end).
        nxt = list(receiver)
        sm = list(receiver)
        cur = list(range(n))          # current position for each start x
        total = list(range(n))        # f(x) accumulated so far
        steps = k
        while steps:
            if steps & 1:
                for x in range(n):
                    c = cur[x]
                    total[x] += sm[c]
                    cur[x] = nxt[c]
            steps >>= 1
            if steps:
                nsm = [0] * n
                nnxt = [0] * n
                for i in range(n):
                    m = nxt[i]
                    nsm[i] = sm[i] + sm[m]
                    nnxt[i] = nxt[m]
                sm, nxt = nsm, nnxt
        return max(total)
