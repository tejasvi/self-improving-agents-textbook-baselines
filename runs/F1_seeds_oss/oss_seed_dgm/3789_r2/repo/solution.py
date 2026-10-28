from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """Return the maximum number of subarrays after removing exactly one conflicting pair.
        
        The array nums is [1, 2, ..., n]. For each pair (a, b) we consider L = min(a, b) and R = max(a, b).
        A subarray [l, r] (1-indexed) contains both elements of the pair iff l <= L and r >= R.
        For a fixed left endpoint l, the furthest we can extend to the right without violating any pair
        is the smallest R among pairs with L >= l (or n+1 if none). That gives the count of valid subarrays
        starting at l as maxR - l + 1 where maxR = minR[l] - 1 (or n when minR[l] is INF).
        
        To consider the effect of removing one pair, we need, for each left index l, the smallest and the
        second‑smallest R among pairs with L >= l. If the pair that provides the smallest R is unique for
        that l, removing it will increase the allowed right bound from minR[l] - 1 to secondR[l] - 1.
        The total increase contributed by a pair i is the sum over all l where i is the unique minimal
        provider of (secondR[l] - minR[l]). The answer is the base total (with no removal) plus the
        maximum increase over all pairs.
        """
        m = len(conflictingPairs)
        INF = n + 1  # sentinel larger than any possible index
        # starts[l] will hold (R, pair_index) for pairs whose left endpoint L equals l
        starts: List[List[tuple[int, int]]] = [[] for _ in range(n + 2)]
        for idx, (a, b) in enumerate(conflictingPairs):
            L = a if a < b else b
            R = b if a < b else a
            starts[L].append((R, idx))

        # Scan from right to left, maintaining the smallest and second smallest R seen so far
        minR = [INF] * (n + 2)      # smallest R for each left index l
        minIdx = [-1] * (n + 2)    # index of the pair giving that smallest R (or -1 if not unique)
        secondR = [INF] * (n + 2)  # second smallest R for each left index l

        curMinR = INF
        curMinIdx = -1
        curSecondR = INF
        # count of pairs sharing the current minimum (used to detect uniqueness)
        curCountMin = 0

        for l in range(n, 0, -1):
            # incorporate pairs that start exactly at l
            for R, idx in starts[l]:
                if R < curMinR:
                    # new strict minimum; old minimum becomes second minimum
                    curSecondR = curMinR
                    curMinR = R
                    curMinIdx = idx
                    curCountMin = 1
                elif R == curMinR:
                    # another pair ties the current minimum -> not unique anymore
                    curCountMin += 1
                    curMinIdx = -1
                    # second minimum stays the same (equal to curMinR)
                    curSecondR = curMinR
                elif R < curSecondR:
                    curSecondR = R
                # else: R is larger than both minima, ignore
            # store results for this l
            minR[l] = curMinR
            minIdx[l] = curMinIdx if curCountMin == 1 else -1
            secondR[l] = curSecondR

        # Base total number of valid subarrays without any removal
        total = 0
        for l in range(1, n + 1):
            maxR = n if minR[l] == INF else minR[l] - 1
            total += maxR - l + 1

        # Compute extra subarrays contributed by removing each pair
        extra = [0] * m
        for l in range(1, n + 1):
            idx = minIdx[l]
            if idx != -1:
                # Removing this pair extends the right bound from minR[l]-1 to secondR[l]-1
                extra[idx] += secondR[l] - minR[l]
        best_extra = max(extra) if extra else 0
        return total + best_extra
