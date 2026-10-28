class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Find the maximum number of groups with strictly increasing lengths.
        
        Strategy:
        - We want to form groups of sizes 1, 2, 3, ..., k
        - Total elements needed for k groups = k(k+1)/2
        - To maximize k, we check if we can form k groups
        - For each number with limit L, when forming k groups, 
          we can use that number at most min(L, k) times
          (since it can appear at most once per group, and there are k groups)
        """
        
        # Sort usage limits in descending order for greedy assignment
        usageLimits.sort(reverse=True)
        
        # Try each possible number of groups k
        # Maximum possible k is limited by the number of distinct elements
        max_possible_k = len(usageLimits)
        
        for k in range(1, max_possible_k + 1):
            # Calculate how many elements are available for k groups
            total_available = 0
            for limit in usageLimits:
                # Each number can be used at most k times (once per group)
                # but limited by its usage limit
                total_available += min(limit, k)
            
            # Check if we have enough elements for k groups
            needed = k * (k + 1) // 2
            
            if total_available < needed:
                # If we can't form k groups, we can't form k+1, k+2, ... either
                return k - 1
        
        # If we successfully formed max_possible_k groups, that's our answer
        return max_possible_k
