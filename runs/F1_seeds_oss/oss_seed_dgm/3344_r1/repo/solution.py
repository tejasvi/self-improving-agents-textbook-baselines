from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        # Transform points to u = x + y and v = x - y
        n = len(points)
        u = [0] * n
        v = [0] * n
        for i, (x, y) in enumerate(points):
            u[i] = x + y
            v[i] = x - y

        # Helper to find max, second max and count of max; similarly min, second min and count
        def get_extremes(arr):
            # max
            max_val = -10**20
            second_max = -10**20
            max_cnt = 0
            # min
            min_val = 10**20
            second_min = 10**20
            min_cnt = 0
            for val in arr:
                # max handling
                if val > max_val:
                    second_max = max_val
                    max_val = val
                    max_cnt = 1
                elif val == max_val:
                    max_cnt += 1
                elif val > second_max:
                    second_max = val
                # min handling
                if val < min_val:
                    second_min = min_val
                    min_val = val
                    min_cnt = 1
                elif val == min_val:
                    min_cnt += 1
                elif val < second_min:
                    second_min = val
            return (max_val, second_max, max_cnt, min_val, second_min, min_cnt)

        max_u, second_max_u, cnt_max_u, min_u, second_min_u, cnt_min_u = get_extremes(u)
        max_v, second_max_v, cnt_max_v, min_v, second_min_v, cnt_min_v = get_extremes(v)

        best = 10**20
        for i in range(n):
            # Determine new extremes after removing point i for u
            if u[i] == max_u:
                new_max_u = max_u if cnt_max_u > 1 else second_max_u
            else:
                new_max_u = max_u
            if u[i] == min_u:
                new_min_u = min_u if cnt_min_u > 1 else second_min_u
            else:
                new_min_u = min_u
            # For v
            if v[i] == max_v:
                new_max_v = max_v if cnt_max_v > 1 else second_max_v
            else:
                new_max_v = max_v
            if v[i] == min_v:
                new_min_v = min_v if cnt_min_v > 1 else second_min_v
            else:
                new_min_v = min_v

            cur = max(new_max_u - new_min_u, new_max_v - new_min_v)
            if cur < best:
                best = cur
        return best
