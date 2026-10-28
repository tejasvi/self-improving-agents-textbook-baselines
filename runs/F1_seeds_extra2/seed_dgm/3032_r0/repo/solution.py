from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: player reached after 2^j passes starting from i
        # sm[i]: sum of ids received during those 2^j passes (excluding start i)
        nxt = list(receiver)
        sm = list(receiver)
        pos = list(range(n))   # current position for each start
        total = list(range(n))  # f(x) accumulated so far, including x
        j = 0
        while (k >> j) > 0:
            if (k >> j) & 1:
                for x in range(n):
                    p = pos[x]
                    total[x] += sm[p]
                    pos[x] = nxt[p]
            if (k >> (j + 1)) > 0:
                sm = [sm[i] + sm[nxt[i]] for i in range(n)]
                nxt = [nxt[nxt[i]] for i in range(n)]
            j += 1
        return max(total)
