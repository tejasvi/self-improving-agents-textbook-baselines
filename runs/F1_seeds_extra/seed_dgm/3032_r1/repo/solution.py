from typing import List


class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        J = list(receiver)          # destination after 2^j passes
        S = list(receiver)          # sum of received ids over 2^j passes
        cur = list(range(n))        # current position for each start
        acc = [0] * n               # accumulated sum for each start
        while k > 0:
            if k & 1:
                for i in range(n):
                    c = cur[i]
                    acc[i] += S[c]
                    cur[i] = J[c]
            k >>= 1
            if k:
                S = [S[x] + S[J[x]] for x in range(n)]
                J = [J[J[x]] for x in range(n)]
        return max(i + acc[i] for i in range(n))
