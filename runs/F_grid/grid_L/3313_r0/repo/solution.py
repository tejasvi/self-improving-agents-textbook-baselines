from typing import List


class Solution:
    def maximumStrength(self, nums: List[int], k: int) -> int:
        # Sentinel for unreachable states; real values are bounded by ~1e15 in magnitude.
        NEG = -(1 << 62)
        # Coefficient of the j-th chosen subarray (1-indexed): (-1)^(j+1) * (k - j + 1)
        w = [0] * (k + 1)
        for j in range(1, k + 1):
            w[j] = (k - j + 1) if j % 2 == 1 else -(k - j + 1)

        f = [NEG] * (k + 1)  # f[j]: best value with j subarrays completed (before/at current index)
        f[0] = 0
        g = [NEG] * (k + 1)  # g[j]: best value with the j-th subarray open and ending at current index
        for x in nums:
            # Descending j: f[j-1] and g[j] still hold values from the previous element.
            for j in range(k, 0, -1):
                cont = g[j] + w[j] * x     # extend the j-th subarray
                start = f[j - 1] + w[j] * x  # start a new j-th subarray at x
                g[j] = cont if cont > start else start
                if g[j] > f[j]:
                    f[j] = g[j]
        return f[k]
