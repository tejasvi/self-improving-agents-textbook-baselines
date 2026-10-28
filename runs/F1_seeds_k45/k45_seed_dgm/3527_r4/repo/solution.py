from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        """
        Handle queries on alternating groups in a circular array of colors.
        
        Query type 1: Count alternating groups of a specific size
        Query type 2: Update a tile's color
        """
        answer = []
        
        def get_alternating_group_sizes():
            """
            Find all maximal alternating group sizes in the circular array.
            Returns a list of sizes of all maximal alternating groups.
            """
            n = len(colors)
            if n == 0:
                return []
            
            sizes = []
            visited = [False] * n
            
            for start in range(n):
                if visited[start]:
                    continue
                
                # Count the length of alternating group starting at 'start'
                length = 1
                current = start
                next_pos = (start + 1) % n
                
                # Extend the group while colors alternate
                while next_pos != start and colors[current] != colors[next_pos]:
                    visited[next_pos] = True
                    length += 1
                    current = next_pos
                    next_pos = (current + 1) % n
                
                visited[start] = True
                sizes.append(length)
            
            return sizes
        
        def count_groups_of_size(size):
            """Count how many maximal alternating groups have the given size."""
            sizes = get_alternating_group_sizes()
            return sum(1 for s in sizes if s == size)
        
        # Process each query
        for query in queries:
            if query[0] == 1:
                # Type 1: Count alternating groups of size query[1]
                size = query[1]
                count = count_groups_of_size(size)
                answer.append(count)
            else:
                # Type 2: Update color at query[1] to query[2]
                index = query[1]
                new_color = query[2]
                colors[index] = new_color
        
        return answer
