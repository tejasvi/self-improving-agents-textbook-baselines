from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # binary lifting up to log2(k) levels
        max_pow = k.bit_length() + 1  # +1 to be safe for k=0
        up = [[0] * n for _ in range(max_pow)]
        sum_val = [[0] * n for _ in range(max_pow)]

        # level 0 corresponds to 1 move
        for i in range(n):
            up[0][i] = receiver[i]
            sum_val[0][i] = receiver[i]

        # build higher powers: 2^p moves
        for p in range(1, max_pow):
            for i in range(n):
                mid = up[p - 1][i]
                up[p][i] = up[p - 1][mid]
                sum_val[p][i] = sum_val[p - 1][i] + sum_val[p - 1][mid]

        best = 0
        for start in range(n):
            cur = start
            total = start  # include the starting player
            remaining = k
            bit = 0
            while remaining:
                if remaining & 1:
                    total += sum_val[bit][cur]
                    cur = up[bit][cur]
                remaining >>= 1
                bit += 1
            if total > best:
                best = total
        return best
