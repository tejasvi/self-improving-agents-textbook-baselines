from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: player reached after 2^j passes from i
        # sm[i]: sum of ids of players receiving during those 2^j passes (excluding i)
        nxt = list(receiver)
        sm = list(receiver)
        cur = list(range(n))  # current position of each starting player
        tot = list(range(n))  # running f(x) for each starting player
        j = 0
        while (k >> j) > 0:
            if (k >> j) & 1:
                for i in range(n):
                    c = cur[i]
                    tot[i] += sm[c]
                    cur[i] = nxt[c]
            if (k >> (j + 1)) == 0:
                break
            # build level j+1
            nsm = [sm[i] + sm[nxt[i]] for i in range(n)]
            nnxt = [nxt[nxt[i]] for i in range(n)]
            sm, nxt = nsm, nnxt
            j += 1
        return max(tot)
