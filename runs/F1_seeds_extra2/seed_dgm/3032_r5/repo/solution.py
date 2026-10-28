from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt: destination after 2^j passes; sm: sum of ids of receivers visited in those passes
        nxt = list(receiver)
        sm = list(receiver)
        cur = list(range(n))   # current position after processed bits
        acc = list(range(n))   # f partial sums, including start id
        while k:
            if k & 1:
                for x in range(n):
                    c = cur[x]
                    acc[x] += sm[c]
                    cur[x] = nxt[c]
            k >>= 1
            if k:
                new_sm = [sm[x] + sm[nxt[x]] for x in range(n)]
                new_nxt = [nxt[nxt[x]] for x in range(n)]
                sm, nxt = new_sm, new_nxt
        return max(acc)
