from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        result = []
        
        # Function to calculate the length of alternating group at each position
        # Returns a list where lengths[i] is the length of the alternating group starting at position i
        def get_alternating_lengths():
            lengths = [0] * n
            for i in range(n):
                if lengths[i] > 0:
                    continue
                # Start of a new alternating group
                length = 1
                j = (i + 1) % n
                while j != i and colors[j] != colors[(j - 1) % n]:
                    length += 1
                    j = (j + 1) % n
                
                # Mark all positions in this group
                for k in range(length):
                    lengths[(i + k) % n] = length
            
            return lengths
        
        # Initial calculation
        lengths = get_alternating_lengths()
        
        for query in queries:
            if query[0] == 1:
                # Type 1: Count alternating groups of given size
                size = query[1]
                count = 0
                seen = set()
                for i in range(n):
                    if lengths[i] == size and i not in seen:
                        count += 1
                        # Mark all positions in this group as seen
                        for k in range(size):
                            seen.add((i + k) % n)
                result.append(count)
            else:
                # Type 2: Update color
                index = query[1]
                new_color = query[2]
                
                if colors[index] != new_color:
                    colors[index] = new_color
                    # Recalculate lengths
                    lengths = get_alternating_lengths()
        
        return result
