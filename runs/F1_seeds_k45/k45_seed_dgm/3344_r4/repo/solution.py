from typing import List

class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        """
        Find the minimum possible maximum Manhattan distance by removing exactly one point.
        
        Key insight: Manhattan distance |x1-x2| + |y1-y2| can be computed as:
        max(|(x1+y1) - (x2+y2)|, |(x1-y1) - (x2-y2)|)
        
        This allows us to compute maximum distance by tracking min/max of transformed coordinates.
        """
        
        n = len(points)
        min_result = float('inf')
        
        # Try removing each point
        for skip_idx in range(n):
            # Calculate maximum distance with this point removed
            max_dist = self._get_max_distance(points, skip_idx)
            min_result = min(min_result, max_dist)
        
        return min_result
    
    def _get_max_distance(self, points: List[List[int]], skip_idx: int) -> int:
        """
        Get the maximum Manhattan distance among points, excluding skip_idx.
        Uses the transformation: |x1-x2| + |y1-y2| = max(|(x1+y1)-(x2+y2)|, |(x1-y1)-(x2-y2)|)
        """
        # Transform points: (x, y) -> (x+y, x-y)
        # We track min/max for both dimensions to get the maximum distance
        
        sum_min = float('inf')  # min of (x+y)
        sum_max = float('-inf')  # max of (x+y)
        diff_min = float('inf')  # min of (x-y)
        diff_max = float('-inf')  # max of (x-y)
        
        for i, (x, y) in enumerate(points):
            if i == skip_idx:
                continue
            
            s = x + y
            d = x - y
            
            sum_min = min(sum_min, s)
            sum_max = max(sum_max, s)
            diff_min = min(diff_min, d)
            diff_max = max(diff_max, d)
        
        # Maximum distance is max of the two ranges
        range_sum = sum_max - sum_min
        range_diff = diff_max - diff_min
        
        return max(range_sum, range_diff)
