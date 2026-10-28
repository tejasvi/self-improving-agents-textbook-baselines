from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # m = number of players counted: the start plus k receivers
        m = k + 1
        nxt = list(receiver)          # nxt[i] = position after 2^j passes from i
        sm = list(range(n))           # sm[i] = sum of the 2^j players visited from i (inclusive of i)
        cur = list(range(n))          # cur[i] = position reached so far from start i
        total = [0] * n               # accumulated sums from start i
        j = 0
        while (m >> j) > 0:
            if (m >> j) & 1:
                total = [t + sm[c] for t, c in zip(total, cur)]
                cur = [nxt[c] for c in cur]
            if (m >> (j + 1)) > 0:
                sm = [a + sm[b] for a, b in zip(sm, nxt)]
                nxt = [nxt[b] for b in nxt]
            j += 1
        return max(total)
