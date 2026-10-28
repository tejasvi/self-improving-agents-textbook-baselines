from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        
        def get_alternating_group_lengths():
            """
            Find all maximal alternating groups in the circular array.
            Returns a list where lengths[i] = length of the maximal alternating group that position i belongs to.
            """
            if n <= 1:
                return [n] * n if n > 0 else []
            
            # First, identify all positions where colors[i] == colors[(i+1) % n]
            # These are the "breaks" in alternating sequences
            
            lengths = [0] * n
            visited = [False] * n
            
            for start in range(n):
                if visited[start]:
                    continue
                
                # Find the length of the alternating group starting at 'start'
                length = 1
                pos = start
                
                # Keep extending while the sequence alternates
                while (pos + 1) % n != start:  # Stop if we've wrapped around to start
                    next_pos = (pos + 1) % n
                    if colors[next_pos] == colors[pos]:
                        # Break in alternation
                        break
                    length += 1
                    pos = next_pos
                
                # Assign this length to all positions in the group
                for i in range(length):
                    idx = (start + i) % n
                    lengths[idx] = length
                    visited[idx] = True
            
            return lengths
        
        def count_groups_of_size(size, lengths):
            """Count unique maximal alternating groups of given size."""
            count = 0
            visited = set()
            
            for i in range(n):
                if i not in visited and lengths[i] == size:
                    # Found a group of the right size starting at position i
                    # Mark all positions in this group as visited
                    for j in range(size):
                        visited.add((i + j) % n)
                    count += 1
            
            return count
        
        result = []
        
        for query in queries:
            if query[0] == 1:
                # Type 1: Count groups of specific size
                size = query[1]
                lengths = get_alternating_group_lengths()
                count = count_groups_of_size(size, lengths)
                result.append(count)
            else:
                # Type 2: Update color
                index = query[1]
                new_color = query[2]
                colors[index] = new_color
        
        return result
