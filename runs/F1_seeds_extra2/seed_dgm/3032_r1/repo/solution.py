from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[v]: node reached after 2^j passes from v
        # sm[v]: sum of ids of the 2^j receivers along the way (excluding v)
        nxt = list(receiver)
        sm = list(receiver)
        pos = list(range(n))       # current position after applied bits
        ans = list(range(n))       # f accumulated so far (includes start)
        while k:
            if k & 1:
                for x in range(n):
                    p = pos[x]
                    ans[x] += sm[p]
                    pos[x] = nxt[p]
            k >>= 1
            if k:
                new_sm = [sm[v] + sm[nxt[v]] for v in range(n)]
                new_nxt = [nxt[nxt[v]] for v in range(n)]
                sm, nxt = new_sm, new_nxt
        return max(ans)
