class Solution:
    def paintWalls(self, cost: List[int], time: List[int]) -> int:
        """
        Paints all walls with minimum cost using a paid and free painter.
        
        Key insight: If paid painter takes T time units, free painter can paint T walls.
        We want to select which walls the paid painter should paint to minimize cost
        while ensuring the free painter (with time availability) can cover the rest.
        
        Strategy:
        1. Sort walls by cost (ascending) - this prioritizes using cheaper walls with paid painter
        2. Iterate through sorted walls, cumulatively adding them to paid painter's work
        3. For each configuration, check if free painter can cover remaining walls
           (remaining walls <= available time from paid painter)
        4. Track minimum cost among all valid configurations
        
        Time complexity: O(n log n) for sorting + O(n) for iteration = O(n log n)
        Space complexity: O(n) for storing wall data
        """
        n = len(cost)
        
        # Create list of (cost, time) tuples and sort by cost (ascending)
        walls = [(cost[i], time[i]) for i in range(n)]
        walls.sort()
        
        min_cost = float('inf')
        time_available = 0
        cost_sum = 0
        
        for i in range(n):
            c, t = walls[i]
            time_available += t
            cost_sum += c
            
            # Number of walls that free painter will paint
            # (all walls except those painted by paid painter)
            free_walls = n - (i + 1)
            
            # Check if free painter can cover remaining walls
            if free_walls <= time_available:
                min_cost = min(min_cost, cost_sum)
        
        return min_cost
