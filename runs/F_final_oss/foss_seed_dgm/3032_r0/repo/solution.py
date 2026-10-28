from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # Number of bits needed to represent k
        max_pow = k.bit_length()  # since we need up to highest bit
        # up[i][v]: node reached from v after 2^i steps
        up = [[0] * n for _ in range(max_pow)]
        # sum[i][v]: sum of node ids visited during those 2^i steps (excluding the starting node v, including each receiver)
        sum_pow = [[0] * n for _ in range(max_pow)]
        # base case: 1 step
        for v in range(n):
            up[0][v] = receiver[v]
            sum_pow[0][v] = receiver[v]
        # build binary lifting tables
        for i in range(1, max_pow):
            prev_up = up[i - 1]
            cur_up = up[i]
            prev_sum = sum_pow[i - 1]
            cur_sum = sum_pow[i]
            for v in range(n):
                mid = prev_up[v]
                cur_up[v] = prev_up[mid]
                cur_sum[v] = prev_sum[v] + prev_sum[mid]
        # compute maximum function value
        best = 0
        for start in range(n):
            total = start  # include starting player id
            cur = start
            remaining = k
            bit = max_pow - 1
            while remaining:
                if remaining >= (1 << bit):
                    total += sum_pow[bit][cur]
                    cur = up[bit][cur]
                    remaining -= (1 << bit)
                bit -= 1
                if bit < 0:
                    break
            if total > best:
                best = total
        return best
