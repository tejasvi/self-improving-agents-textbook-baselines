from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        result = []
        
        # Helper function to compute lengths of alternating groups
        def compute_group_lengths():
            """
            Compute the length of alternating group starting at each position.
            group_lengths[i] = length of alternating group starting at index i
            """
            lengths = [1] * n
            
            for i in range(n):
                if lengths[i] > 1:
                    continue
                    
                # Start from position i and count how many consecutive alternating tiles
                j = i
                count = 1
                while count < n and colors[(j + count) % n] != colors[(j + count - 1) % n]:
                    count += 1
                
                # Mark all positions in this group with the group length
                for k in range(count):
                    lengths[(i + k) % n] = count
            
            return lengths
        
        # Initial computation
        group_lengths = compute_group_lengths()
        
        # Process queries
        for query in queries:
            if query[0] == 1:
                # Type 1: Count alternating groups with specific size
                size = query[1]
                count = 0
                for i in range(n):
                    if group_lengths[i] == size:
                        count += 1
                result.append(count)
            else:
                # Type 2: Update color at index
                idx, new_color = query[1], query[2]
                
                # Only recompute if color actually changes
                if colors[idx] != new_color:
                    colors[idx] = new_color
                    group_lengths = compute_group_lengths()
        
        return result
