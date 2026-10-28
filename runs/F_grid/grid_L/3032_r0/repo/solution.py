from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player reached after 2^j passes from i
        # sm[j][i]: sum of ids of the 2^j players i, r(i), ..., r^(2^j - 1)(i)
        nxt = [list(receiver)]
        sm = [list(range(n))]
        j = 0
        while (1 << (j + 1)) <= k:
            prev_nxt = nxt[j]
            prev_sm = sm[j]
            new_nxt = [prev_nxt[prev_nxt[i]] for i in range(n)]
            new_sm = [prev_sm[i] + prev_sm[prev_nxt[i]] for i in range(n)]
            nxt.append(new_nxt)
            sm.append(new_sm)
            j += 1

        best = 0
        for x in range(n):
            total = 0
            cur = x
            bit = 0
            kk = k
            while kk:
                if kk & 1:
                    total += sm[bit][cur]
                    cur = nxt[bit][cur]
                kk >>= 1
                bit += 1
            total += cur  # the k-th receiver's id (terms x..r^k(x))
            if total > best:
                best = total
        return best
