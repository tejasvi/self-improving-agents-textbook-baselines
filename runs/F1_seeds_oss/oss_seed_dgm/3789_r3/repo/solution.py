from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs so that lo < hi and store by lo index.
        m = len(conflictingPairs)
        adj = [[] for _ in range(n + 2)]  # adj[lo] = list of (hi, pair_index)
        for idx, (a, b) in enumerate(conflictingPairs):
            if a < b:
                lo, hi = a, b
            else:
                lo, hi = b, a
            adj[lo].append((hi, idx))
        INF = n + 1  # sentinel value larger than any possible hi
        # Variables to keep track of smallest and second smallest hi among active pairs
        min1 = INF
        cnt1 = 0  # how many pairs have hi == min1
        min1_idx = -1  # index of the unique minimal pair when cnt1 == 1
        min2 = INF
        cnt2 = 0
        total = 0  # total valid subarrays with all pairs present
        gain = [0] * m  # additional subarrays obtained if we remove this pair
        # Sweep left border L from n down to 1, adding pairs whose lo == L
        for L in range(n, 0, -1):
            for hi, idx in adj[L]:
                # Insert hi into the multiset maintaining min1 and min2
                if hi < min1:
                    # shift current min1 to second min
                    min2, cnt2 = min1, cnt1
                    min1, cnt1, min1_idx = hi, 1, idx
                elif hi == min1:
                    cnt1 += 1
                elif hi < min2:
                    min2, cnt2 = hi, 1
                elif hi == min2:
                    cnt2 += 1
            # Number of valid subarrays starting at L
            if min1 == INF:
                total += n - L + 1
            else:
                total += min1 - L
                # If the minimal hi is unique, removing that pair would allow extending
                # the right border up to the second minimal (or to n+1 if none).
                if cnt1 == 1:
                    second = min2 if min2 != INF else INF
                    delta = second - min1
                    gain[min1_idx] += delta
        # Best improvement by removing a single pair
        best_gain = max(gain) if gain else 0
        return total + best_gain
