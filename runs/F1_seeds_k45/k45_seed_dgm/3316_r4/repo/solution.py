from typing import List

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Sort the array
        nums.sort()
        
        result = 0
        
        # For each pair of indices (i, j) where i < j,
        # count how many subsequences of length k have their minimum power as nums[j] - nums[i]
        
        for i in range(n):
            for j in range(i + 1, n):
                min_diff = nums[j] - nums[i]
                
                # Count subsequences where:
                # 1. Both nums[i] and nums[j] are included
                # 2. No elements strictly between i and j are included (ensures this is the min)
                # 3. All other selected elements have difference >= min_diff from all neighbors
                # 4. Total length is k
                
                count = self._count_with_pair(nums, k, i, j, min_diff)
                result = (result + count * min_diff) % MOD
        
        return result
    
    def _count_with_pair(self, nums: List[int], k: int, i: int, j: int, min_diff: int) -> int:
        """
        Count subsequences of length k that:
        - Include both nums[i] and nums[j]
        - No elements between indices i and j are included
        - All consecutive elements differ by >= min_diff
        - The minimum difference is exactly min_diff
        """
        MOD = 10**9 + 7
        n = len(nums)
        
        if k == 2:
            return 1
        
        # We need k-2 more elements from [0, i-1] U [j+1, n-1]
        # Where each element satisfies the distance requirement from its neighbors
        
        # Elements from [0, i-1] that are valid:
        # nums[i] - nums[idx] >= min_diff
        left_candidates = []
        for idx in range(i):
            if nums[i] - nums[idx] >= min_diff:
                left_candidates.append(idx)
        
        # Elements from [j+1, n-1] that are valid:
        # nums[idx] - nums[j] >= min_diff
        right_candidates = []
        for idx in range(j + 1, n):
            if nums[idx] - nums[j] >= min_diff:
                right_candidates.append(idx)
        
        # Now count ways to pick k-2 elements from left_candidates + right_candidates
        # such that consecutive picks differ by >= min_diff
        
        return self._count_ways(nums, left_candidates, right_candidates, k - 2, min_diff)
    
    def _count_ways(self, nums: List[int], left_indices: List[int], right_indices: List[int], 
                    need: int, min_diff: int) -> int:
        """
        Count ways to pick 'need' elements from left_indices and right_indices
        such that all consecutive elements (in sorted order) differ by >= min_diff.
        """
        MOD = 10**9 + 7
        
        # Combine and sort all candidate indices
        all_indices = sorted(left_indices + right_indices)
        
        if need == 0:
            return 1
        
        if len(all_indices) < need:
            return 0
        
        m = len(all_indices)
        
        # DP: dp[i][j] = ways to pick j elements from first i candidate indices
        # such that all consecutive selected elements differ by >= min_diff
        
        dp = [[0] * (need + 1) for _ in range(m + 1)]
        
        # Base case
        for i in range(m + 1):
            dp[i][0] = 1
        
        for i in range(1, m + 1):
            curr_idx = all_indices[i - 1]
            
            for j in range(1, min(i + 1, need + 1)):
                # Option 1: Don't pick current element
                dp[i][j] = dp[i - 1][j]
                
                # Option 2: Pick current element
                if j == 1:
                    dp[i][j] = (dp[i][j] + 1) % MOD
                else:
                    # We need to pick j-1 elements from some previous positions
                    # such that the last picked element differs from curr_idx by >= min_diff
                    for prev_i in range(1, i):
                        prev_idx = all_indices[prev_i - 1]
                        if nums[curr_idx] - nums[prev_idx] >= min_diff:
                            dp[i][j] = (dp[i][j] + dp[prev_i][j - 1]) % MOD
        
        return dp[m][need]
