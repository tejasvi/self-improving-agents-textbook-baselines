from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt: destination after 2^j passes; sm: sum of ids received in those 2^j passes
        nxt = list(receiver)
        sm = list(receiver)
        pos = list(range(n))       # current position after processed bits
        total = list(range(n))     # f partial sums, starting with x itself
        while k:
            if k & 1:
                for x in range(n):
                    p = pos[x]
                    total[x] += sm[p]
                    pos[x] = nxt[p]
            k >>= 1
            if k:
                new_sm = [sm[i] + sm[nxt[i]] for i in range(n)]
                nxt = [nxt[nxt[i]] for i in range(n)]
                sm = new_sm
        return max(total)
