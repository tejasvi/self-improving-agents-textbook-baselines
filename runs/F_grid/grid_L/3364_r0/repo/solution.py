from typing import List


class Solution:
    def minimumValueSum(self, nums: List[int], andValues: List[int]) -> int:
        INF = float("inf")
        n = len(nums)
        m = len(andValues)

        # dp_prev[i]: min sum using j-1 subarrays covering nums[0:i]
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0

        for j in range(m):
            target = andValues[j]
            dp_cur = [INF] * (n + 1)
            # groups: list of [and_value, min dp_prev[l]] over start indices l
            # (l in 0..r), with equal AND values merged; ordered by start index.
            groups = []
            for r in range(n):
                x = nums[r]
                # extend all existing windows to include nums[r]
                new_groups = []
                for v, mn in groups:
                    nv = v & x
                    if new_groups and new_groups[-1][0] == nv:
                        if mn < new_groups[-1][1]:
                            new_groups[-1][1] = mn
                    else:
                        new_groups.append([nv, mn])
                # new window starting at l = r (uses dp_prev[r] elements before)
                if dp_prev[r] < INF:
                    if new_groups and new_groups[-1][0] == x:
                        if dp_prev[r] < new_groups[-1][1]:
                            new_groups[-1][1] = dp_prev[r]
                    else:
                        new_groups.append([x, dp_prev[r]])
                groups = new_groups

                best = INF
                for v, mn in groups:
                    if v == target and mn < best:
                        best = mn
                if best < INF:
                    dp_cur[r + 1] = best + x
            dp_prev = dp_cur

        return -1 if dp_prev[n] == INF else int(dp_prev[n])
