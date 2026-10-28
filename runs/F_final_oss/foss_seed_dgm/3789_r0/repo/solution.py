from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Convert each pair to an interval [L, R] where L = min(a,b), R = max(a,b)
        m = len(conflictingPairs)
        L = [0] * m
        R = [0] * m
        start_at = [[] for _ in range(n + 2)]  # 1-indexed
        for idx, (a, b) in enumerate(conflictingPairs):
            l = a if a < b else b
            r = b if a < b else a
            L[idx] = l
            R[idx] = r
            start_at[l].append(idx)

        INF = n + 1  # value larger than any possible R
        # suffix minima for R and second minima
        min1_arr = [INF] * (n + 2)
        min2_arr = [INF] * (n + 2)
        idx1_arr = [-1] * (n + 2)
        # current bests while sweeping from right to left
        cur_min1 = INF
        cur_idx1 = -1
        cur_min2 = INF
        cur_idx2 = -1
        for pos in range(n, 0, -1):
            # incorporate intervals that start at this position
            for idx in start_at[pos]:
                r = R[idx]
                if r < cur_min1:
                    cur_min2, cur_idx2 = cur_min1, cur_idx1
                    cur_min1, cur_idx1 = r, idx
                elif r < cur_min2:
                    cur_min2, cur_idx2 = r, idx
            min1_arr[pos] = cur_min1
            min2_arr[pos] = cur_min2
            idx1_arr[pos] = cur_idx1

        # base total using the first minima (or INF meaning no restriction)
        base_total = 0
        for l in range(1, n + 1):
            limit_plus_one = min1_arr[l] if min1_arr[l] != INF else INF
            base_total += limit_plus_one - l

        # compute delta for each interval when it is removed
        delta = [0] * m
        for l in range(1, n + 1):
            idx = idx1_arr[l]
            if idx == -1:
                continue
            second = min2_arr[l] if min2_arr[l] != INF else INF
            diff = second - min1_arr[l]
            delta[idx] += diff

        # answer is the maximum total after removing exactly one conflicting pair
        best = max(base_total + d for d in delta)
        return best
