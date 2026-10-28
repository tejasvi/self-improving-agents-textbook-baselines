from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # nxt[j][i]: player reached after 2^j passes from i
        # sm[j][i]: sum of ids of the 2^j players that receive the ball starting from i
        #           (excluding i itself, including the 2^j-th receiver)
        nxt = [list(receiver)]
        sm = [list(receiver)]
        j = 1
        while (1 << j) <= k:
            prev_n = nxt[-1]
            prev_s = sm[-1]
            cur_n = [0] * n
            cur_s = [0] * n
            for i in range(n):
                mid = prev_n[i]
                cur_n[i] = prev_n[mid]
                cur_s[i] = prev_s[i] + prev_s[mid]
            nxt.append(cur_n)
            sm.append(cur_s)
            j += 1

        best = 0
        levels = len(nxt)
        for x in range(n):
            total = x
            cur = x
            kk = k
            b = 0
            while kk:
                if kk & 1:
                    total += sm[b][cur]
                    cur = nxt[b][cur]
                kk >>= 1
                b += 1
            if total > best:
                best = total
        return best
