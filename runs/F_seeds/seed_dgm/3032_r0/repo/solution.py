from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: player reached after 2^j passes starting at i
        # sm[i]: sum of ids of receivers over those 2^j passes (excluding i)
        nxt = list(receiver)
        sm = list(receiver)
        cur = list(range(n))       # current position for each start x
        total = [0] * n            # accumulated pass-id sums for each start x

        j = 0
        while (k >> j) > 0:
            if (k >> j) & 1:
                for x in range(n):
                    c = cur[x]
                    total[x] += sm[c]
                    cur[x] = nxt[c]
            if (k >> (j + 1)) > 0:
                new_sm = [sm[i] + sm[nxt[i]] for i in range(n)]
                new_nxt = [nxt[nxt[i]] for i in range(n)]
                sm, nxt = new_sm, new_nxt
            j += 1

        return max(x + total[x] for x in range(n))
