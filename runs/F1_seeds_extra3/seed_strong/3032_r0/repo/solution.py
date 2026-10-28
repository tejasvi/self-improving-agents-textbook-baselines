from typing import *


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        nxt = list(receiver)        # position after 2^j passes
        S = list(receiver)          # sum of ids received in the first 2^j passes
        cur = list(range(n))        # current position of each start
        total = list(range(n))      # f(x) accumulated so far (includes x)
        while k:
            if k & 1:
                total = [t + S[c] for t, c in zip(total, cur)]
                cur = [nxt[c] for c in cur]
            k >>= 1
            if k:
                S = [s + S[j] for s, j in zip(S, nxt)]
                nxt = [nxt[j] for j in nxt]
        return max(total)
