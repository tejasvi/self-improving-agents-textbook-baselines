from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        """
        Process queries on alternating groups of tiles.
        
        Type 1 query: Count alternating groups of size k
        Type 2 query: Update a tile color
        """
        n = len(colors)
        
        # Helper function to count alternating groups of size k
        def count_groups(size):
            """Count all alternating groups of the given size"""
            if size > n:
                return 0
            
            count = 0
            visited = [False] * n
            
            for i in range(n):
                if visited[i]:
                    continue
                
                # Find the maximal alternating segment starting from i
                segment_start = i
                segment_length = 1
                j = (i + 1) % n
                
                # Extend the segment while colors alternate
                while j != i and colors[(j - 1) % n] != colors[j]:
                    segment_length += 1
                    visited[j] = True
                    j = (j + 1) % n
                
                visited[i] = True
                
                # Count how many groups of the given size can fit in this segment
                if segment_length >= size:
                    # Number of groups of size k in a segment of length L is max(0, L - k + 1)
                    # But if the segment wraps around (j == i), we need special handling
                    if j == i:  # Full circle is alternating
                        count += segment_length
                    else:
                        count += max(0, segment_length - size + 1)
            
            return count
        
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Type 1: Count groups of size query[1]
                size = query[1]
                result.append(count_groups(size))
            else:
                # Type 2: Update color
                idx = query[1]
                new_color = query[2]
                colors[idx] = new_color
        
        return result
