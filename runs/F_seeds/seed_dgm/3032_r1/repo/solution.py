from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player reached after 2^j passes from i
        # sm[j][i]: sum of the ids received during those 2^j passes (excluding i)
        nxt = [list(receiver)]
        sm = [list(receiver)]
        j = 0
        while (1 << (j + 1)) <= k:
            prev_n = nxt[j]
            prev_s = sm[j]
            new_n = [prev_n[prev_n[i]] for i in range(n)]
            new_s = [prev_s[i] + prev_s[prev_n[i]] for i in range(n)]
            nxt.append(new_n)
            sm.append(new_s)
            j += 1

        best = 0
        for x in range(n):
            total = x
            cur = x
            bit = 0
            rem = k
            while rem:
                if rem & 1:
                    total += sm[bit][cur]
                    cur = nxt[bit][cur]
                rem >>= 1
                bit += 1
            if total > best:
                best = total
        return best
