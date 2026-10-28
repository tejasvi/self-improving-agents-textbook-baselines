from typing import List

class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        n = len(receiver)
        # maximum power needed (2^LOG > k)
        LOG = k.bit_length()  # since k up to 1e10, ~34 bits
        # up[p][i]: node reached from p after 2^i steps
        up = [[0] * n for _ in range(LOG)]
        # sum[p][i]: sum of node ids visited during those 2^i steps (excluding the starting node, including each receiver)
        sum_table = [[0] * n for _ in range(LOG)]
        # i = 0 corresponds to 1 step
        for v in range(n):
            up[0][v] = receiver[v]
            sum_table[0][v] = receiver[v]
        for i in range(1, LOG):
            prev_up = up[i-1]
            prev_sum = sum_table[i-1]
            cur_up = up[i]
            cur_sum = sum_table[i]
            for v in range(n):
                mid = prev_up[v]
                cur_up[v] = prev_up[mid]
                cur_sum[v] = prev_sum[v] + prev_sum[mid]
        max_val = 0
        for start in range(n):
            total = start
            cur = start
            steps = k
            bit = 0
            while steps:
                if steps & 1:
                    total += sum_table[bit][cur]
                    cur = up[bit][cur]
                steps >>= 1
                bit += 1
            if total > max_val:
                max_val = total
        return max_val
