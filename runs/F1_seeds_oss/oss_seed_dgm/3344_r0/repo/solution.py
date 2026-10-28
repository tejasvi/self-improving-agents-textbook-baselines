from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        n = len(points)
        # Transformations for Manhattan distance
        # t0 = x + y, t1 = x - y, t2 = -x + y, t3 = -x - y
        trans = [[0] * n for _ in range(4)]
        for i, (x, y) in enumerate(points):
            trans[0][i] = x + y
            trans[1][i] = x - y
            trans[2][i] = -x + y
            trans[3][i] = -x - y

        # For each transformation keep top two max and min values with their indices
        max_vals = []  # each entry: (max1_val, max1_idx, max2_val)
        min_vals = []  # each entry: (min1_val, min1_idx, min2_val)
        for t in range(4):
            arr = trans[t]
            # create list of (value, idx)
            pairs = [(val, idx) for idx, val in enumerate(arr)]
            pairs.sort(key=lambda x: x[0])  # ascending
            # mins
            min1_val, min1_idx = pairs[0]
            # second smallest (could be same index if duplicates but that's fine)
            min2_val = pairs[1][0] if n > 1 else min1_val
            min_vals.append((min1_val, min1_idx, min2_val))
            # maxes
            max1_val, max1_idx = pairs[-1]
            max2_val = pairs[-2][0] if n > 1 else max1_val
            max_vals.append((max1_val, max1_idx, max2_val))

        best = float('inf')
        for i in range(n):
            cur_max_dist = 0
            for t in range(4):
                max1_val, max1_idx, max2_val = max_vals[t]
                min1_val, min1_idx, min2_val = min_vals[t]
                # choose max/min that does not involve point i
                cur_max = max1_val if max1_idx != i else max2_val
                cur_min = min1_val if min1_idx != i else min2_val
                diff = cur_max - cur_min
                if diff > cur_max_dist:
                    cur_max_dist = diff
                if cur_max_dist >= best:
                    break
            if cur_max_dist < best:
                best = cur_max_dist
        return int(best)
