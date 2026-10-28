from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        
        # Calculate initial alternating group lengths
        # group_lengths[i] = length of alternating group starting at position i
        group_lengths = self._calculate_group_lengths(colors)
        
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Type 1: Count alternating groups of size query[1]
                size = query[1]
                count = sum(1 for length in group_lengths if length == size)
                result.append(count)
            else:
                # Type 2: Update color at index query[1] to query[2]
                index = query[1]
                new_color = query[2]
                
                if colors[index] != new_color:
                    colors[index] = new_color
                    # Recalculate affected group lengths
                    group_lengths = self._calculate_group_lengths(colors)
        
        return result
    
    def _calculate_group_lengths(self, colors: List[int]) -> List[int]:
        """
        Calculate the length of each alternating group.
        Returns a list where group_lengths[i] is the length of the alternating
        group that starts at position i (and wraps around if needed).
        """
        n = len(colors)
        group_lengths = []
        visited = [False] * n
        
        for i in range(n):
            if not visited[i]:
                # Find the length of the alternating group starting at i
                length = 1
                j = (i + 1) % n
                
                # Stop if we've seen all elements (entire array is one group)
                # or if we've formed a complete group
                while j != i and length < n and colors[j] != colors[j - 1]:
                    length += 1
                    j = (j + 1) % n
                
                # Mark all positions in this group as visited
                for k in range(length):
                    visited[(i + k) % n] = True
                
                group_lengths.append(length)
        
        return group_lengths
