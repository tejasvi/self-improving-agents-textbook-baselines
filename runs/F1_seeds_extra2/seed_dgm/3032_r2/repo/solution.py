from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[x]: player reached after 2^j passes from x
        # sm[x]: sum of ids of players receiving during those 2^j passes (excluding x)
        nxt = list(receiver)
        sm = list(receiver)
        pos = list(range(n))        # current position after jumps taken so far
        total = list(range(n))      # f contribution: x plus sums of jumps taken
        kk = k
        while kk:
            if kk & 1:
                for x in range(n):
                    p = pos[x]
                    total[x] += sm[p]
                    pos[x] = nxt[p]
            kk >>= 1
            if kk:
                new_sm = [s + sm[m] for s, m in zip(sm, nxt)]
                new_nxt = [nxt[m] for m in nxt]
                sm, nxt = new_sm, new_nxt
        return max(total)
