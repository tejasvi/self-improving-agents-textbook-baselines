from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        # Transform each point to two coordinates p = x + y and q = x - y.
        # The maximum Manhattan distance among a set of points equals max(
        #     max(p) - min(p),
        #     max(q) - min(q)
        # ).
        n = len(points)
        # Store p and q values with original indices.
        p_vals = []  # list of (value, index)
        q_vals = []
        for i, (x, y) in enumerate(points):
            p = x + y
            q = x - y
            p_vals.append((p, i))
            q_vals.append((q, i))
        # Helper to get top two max and min values with indices.
        def top_two(vals, reverse=False):
            # Return list of up to two (value, index) sorted according to reverse flag.
            # reverse=False -> smallest first; reverse=True -> largest first.
            # We can simply sort once; O(n log n) is fine for 1e5, but we can do linear scan.
            # Use linear scan for O(n).
            best1 = (float('inf'), -1) if not reverse else (float('-inf'), -1)
            best2 = (float('inf'), -1) if not reverse else (float('-inf'), -1)
            for v, idx in vals:
                if not reverse:
                    if v < best1[0]:
                        best2 = best1
                        best1 = (v, idx)
                    elif v < best2[0]:
                        best2 = (v, idx)
                else:
                    if v > best1[0]:
                        best2 = best1
                        best1 = (v, idx)
                    elif v > best2[0]:
                        best2 = (v, idx)
            # Filter out placeholder entries.
            res = []
            if best1[1] != -1:
                res.append(best1)
            if best2[1] != -1:
                res.append(best2)
            return res
        # Get extremes.
        min_p_two = top_two(p_vals, reverse=False)  # smallest
        max_p_two = top_two(p_vals, reverse=True)   # largest
        min_q_two = top_two(q_vals, reverse=False)
        max_q_two = top_two(q_vals, reverse=True)
        # Collect candidate indices that could affect the overall max distance.
        candidates = set()
        for _, idx in min_p_two + max_p_two + min_q_two + max_q_two:
            candidates.add(idx)
        # Pre-compute overall extremes for quick lookup.
        overall_min_p = min_p_two[0][0]
        overall_max_p = max_p_two[0][0]
        overall_min_q = min_q_two[0][0]
        overall_max_q = max_q_two[0][0]
        # For each candidate removal, compute new extremes.
        best = float('inf')
        for rem in candidates:
            # Determine new min and max for p.
            if rem == min_p_two[0][1]:
                new_min_p = min_p_two[1][0] if len(min_p_two) > 1 else overall_max_p  # fallback: if all points same, use same value.
            else:
                new_min_p = overall_min_p
            if rem == max_p_two[0][1]:
                new_max_p = max_p_two[1][0] if len(max_p_two) > 1 else overall_min_p
            else:
                new_max_p = overall_max_p
            # For q.
            if rem == min_q_two[0][1]:
                new_min_q = min_q_two[1][0] if len(min_q_two) > 1 else overall_max_q
            else:
                new_min_q = overall_min_q
            if rem == max_q_two[0][1]:
                new_max_q = max_q_two[1][0] if len(max_q_two) > 1 else overall_min_q
            else:
                new_max_q = overall_max_q
            cur = max(new_max_p - new_min_p, new_max_q - new_min_q)
            if cur < best:
                best = cur
        return best
