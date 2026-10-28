from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        # Transform points to p = x + y and q = x - y.
        n = len(points)
        p = [0] * n
        q = [0] * n
        for i, (x, y) in enumerate(points):
            p[i] = x + y
            q[i] = x - y

        # Helper to compute max, second max, min, second min and counts.
        def compute_extremes(arr):
            max_val = -10**20
            min_val = 10**20
            second_max = -10**20
            second_min = 10**20
            max_cnt = 0
            min_cnt = 0
            for v in arr:
                # max and second max
                if v > max_val:
                    second_max = max_val
                    max_val = v
                    max_cnt = 1
                elif v == max_val:
                    max_cnt += 1
                elif v > second_max:
                    second_max = v
                # min and second min
                if v < min_val:
                    second_min = min_val
                    min_val = v
                    min_cnt = 1
                elif v == min_val:
                    min_cnt += 1
                elif v < second_min:
                    second_min = v
            return max_val, second_max, max_cnt, min_val, second_min, min_cnt

        max_p, sec_max_p, cnt_max_p, min_p, sec_min_p, cnt_min_p = compute_extremes(p)
        max_q, sec_max_q, cnt_max_q, min_q, sec_min_q, cnt_min_q = compute_extremes(q)

        best = 10**30
        for i in range(n):
            # Determine extremes after removing point i.
            cur_max_p = max_p if (p[i] != max_p or cnt_max_p > 1) else sec_max_p
            cur_min_p = min_p if (p[i] != min_p or cnt_min_p > 1) else sec_min_p
            cur_max_q = max_q if (q[i] != max_q or cnt_max_q > 1) else sec_max_q
            cur_min_q = min_q if (q[i] != min_q or cnt_min_q > 1) else sec_min_q

            # In the rare case where sec_max or sec_min remain at initial extreme values
            # (which can happen when all points have the same p or q), fallback to the
            # current max/min because the distance will be zero.
            if cur_max_p == -10**20:
                cur_max_p = cur_min_p
            if cur_min_p == 10**20:
                cur_min_p = cur_max_p
            if cur_max_q == -10**20:
                cur_max_q = cur_min_q
            if cur_min_q == 10**20:
                cur_min_q = cur_max_q

            candidate = max(cur_max_p - cur_min_p, cur_max_q - cur_min_q)
            if candidate < best:
                best = candidate
        return best
