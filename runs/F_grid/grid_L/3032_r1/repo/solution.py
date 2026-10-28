from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player reached after 2^j passes from i
        # sm[j][i]: sum of ids received during those 2^j passes (excluding i itself)
        nxt = [list(receiver)]
        sm = [list(receiver)]
        levels = k.bit_length()
        for j in range(1, levels):
            pn = nxt[j - 1]
            ps = sm[j - 1]
            nxt.append([pn[pn[i]] for i in range(n)])
            sm.append([ps[i] + ps[pn[i]] for i in range(n)])

        best = 0
        for x in range(n):
            total = x
            cur = x
            kk = k
            j = 0
            while kk:
                if kk & 1:
                    total += sm[j][cur]
                    cur = nxt[j][cur]
                kk >>= 1
                j += 1
            if total > best:
                best = total
        return best
