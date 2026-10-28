class Solution:
    def maxIncreasingGroups(self, usageLimits: List[int]) -> int:
        """
        Create the maximum number of groups where:
        - Each group has distinct numbers
        - Group i has size > group i-1
        - Number j is used at most usageLimits[j] times
        
        Strategy: Use a greedy approach with a min-heap
        - Try to form groups of size 1, 2, 3, ...
        - For each group of size k, pick k numbers with highest remaining usage
        - Use a min-heap to efficiently track and update usage counts
        """
        import heapq
        
        # Use a max-heap (negate values for min-heap in Python)
        # Store negative values to simulate max-heap
        heap = [-limit for limit in usageLimits]
        heapq.heapify(heap)
        
        groups = 0
        group_size = 1
        
        while True:
            # For this group, we need group_size distinct numbers
            # Take the group_size numbers with the highest remaining usage
            temp = []
            
            # Pop group_size elements to use in this group
            for _ in range(group_size):
                if not heap:
                    # Not enough numbers available
                    return groups
                temp.append(heapq.heappop(heap))
            
            # Check if we actually have group_size numbers available
            # temp contains negative values, so check the most restrictive (smallest absolute value)
            min_usage = -temp[-1]  # The last popped element has the smallest count
            
            if min_usage == 0:
                # At least one number has 0 usage left, can't form this group
                return groups
            
            # We can form this group, so decrease usage by 1 for each number used
            for i in range(len(temp)):
                # Decrease the usage and push back
                heapq.heappush(heap, temp[i] + 1)  # Add 1 because we're using negatives
            
            groups += 1
            group_size += 1
