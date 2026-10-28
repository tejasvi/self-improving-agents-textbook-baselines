from typing import List


class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        NEG = -(10 ** 30)
        # w[j] for j = 1..k: weight of the j-th chosen subarray
        w = [0] * (k + 1)
        for j in range(1, k + 1):
            sign = 1 if j % 2 == 1 else -1
            w[j] = sign * (k - j + 1)

        # end[j]: best value using exactly j finished subarrays (none open)
        # cur[j]: best value where j-th subarray is open and contains current element
        end = [NEG] * (k + 1)
        end[0] = 0
        cur = [NEG] * (k + 1)

        for x in nums:
            new_cur = [NEG] * (k + 1)
            for j in range(1, k + 1):
                best_prev = cur[j] if cur[j] > end[j - 1] else end[j - 1]
                if best_prev > NEG:
                    new_cur[j] = best_prev + w[j] * x
            new_end = end[:]
            for j in range(1, k + 1):
                if new_cur[j] > new_end[j]:
                    new_end[j] = new_cur[j]
            end = new_end
            cur = new_cur

        return end[k]
