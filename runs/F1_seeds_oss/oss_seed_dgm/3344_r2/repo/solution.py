from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """Return the minimal possible maximum Manhattan distance after removing exactly one point.

        The Manhattan distance between two points (x1, y1) and (x2, y2) is |x1-x2| + |y1-y2|.
        For a set of points, the maximum Manhattan distance can be expressed as the maximum
        difference among the transformed coordinates x+y and x-y:
            max_dist = max( max(x+y) - min(x+y), max(x-y) - min(x-y) )
        To evaluate the effect of removing each point, we keep track of the largest and
        second‑largest (as well as smallest and second‑smallest) values of these transforms.
        For each point we recompute the range using the appropriate substitute when the
        point contributes to an extreme.
        The overall answer is the minimum of these candidate maximum distances.
        """
        n = len(points)
        # Transform coordinates
        a = []  # x + y
        b = []  # x - y
        for x, y in points:
            a.append(x + y)
            b.append(x - y)

        # Helper to compute max, count of max, second max, min, count of min, second min
        def extrema(arr):
            max_val = -10**20
            min_val = 10**20
            count_max = 0
            count_min = 0
            second_max = -10**20
            second_min = 10**20
            for v in arr:
                # max handling
                if v > max_val:
                    second_max = max_val
                    max_val = v
                    count_max = 1
                elif v == max_val:
                    count_max += 1
                elif v > second_max:
                    second_max = v
                # min handling
                if v < min_val:
                    second_min = min_val
                    min_val = v
                    count_min = 1
                elif v == min_val:
                    count_min += 1
                elif v < second_min:
                    second_min = v
            # If there was no second distinct value, set second to same as extreme
            if count_max == n:
                second_max = max_val
            if count_min == n:
                second_min = min_val
            return max_val, count_max, second_max, min_val, count_min, second_min

        max_a, cnt_max_a, sec_max_a, min_a, cnt_min_a, sec_min_a = extrema(a)
        max_b, cnt_max_b, sec_max_b, min_b, cnt_min_b, sec_min_b = extrema(b)

        best = 10**20
        for i in range(n):
            # Determine max/min after removing point i for transformed a
            cur_max_a = sec_max_a if (a[i] == max_a and cnt_max_a == 1) else max_a
            cur_min_a = sec_min_a if (a[i] == min_a and cnt_min_a == 1) else min_a
            range_a = cur_max_a - cur_min_a

            cur_max_b = sec_max_b if (b[i] == max_b and cnt_max_b == 1) else max_b
            cur_min_b = sec_min_b if (b[i] == min_b and cnt_min_b == 1) else min_b
            range_b = cur_max_b - cur_min_b

            candidate = max(range_a, range_b)
            if candidate < best:
                best = candidate
        return best
