from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[i]: position after 2^j steps from i
        # sm[i]: sum of the 2^j nodes visited starting at i (i, r(i), ..., r^(2^j - 1)(i))
        nxt = list(receiver)
        sm = list(range(n))
        # cur[x]: current position of ball path for start x; tot[x]: sum of nodes passed so far
        cur = list(range(n))
        tot = [0] * n
        bit = 0
        while (k >> bit) > 0:
            if (k >> bit) & 1:
                tot = [t + sm[c] for t, c in zip(tot, cur)]
                cur = [nxt[c] for c in cur]
            if (k >> (bit + 1)) > 0:
                new_sm = [s + sm[nxt[i]] for i, s in enumerate(sm)]
                new_nxt = [nxt[nxt[i]] for i in range(n)]
                sm, nxt = new_sm, new_nxt
            bit += 1
        # tot = r^0(x)+...+r^(k-1)(x), cur = r^k(x)
        return max(t + c for t, c in zip(tot, cur))
