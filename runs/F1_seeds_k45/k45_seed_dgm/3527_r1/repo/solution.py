class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        result = []
        
        def get_alternating_groups():
            """
            Returns a list of lengths of all alternating groups in the circular array.
            """
            groups = []
            i = 0
            
            # Check if the entire array is one alternating group
            all_alternating = True
            for j in range(n):
                if colors[j] == colors[(j + 1) % n]:
                    all_alternating = False
                    break
            
            if all_alternating:
                # The entire circle is one alternating group
                return [n]
            
            # Find all alternating groups
            visited = [False] * n
            while i < n:
                if visited[i]:
                    i += 1
                    continue
                
                # Start of a potential group
                start = i
                length = 1
                visited[i] = True
                j = (i + 1) % n
                
                # Extend the group while colors alternate
                while j != start and colors[j] != colors[(j - 1) % n]:
                    visited[j] = True
                    length += 1
                    j = (j + 1) % n
                
                if length > 1:
                    groups.append(length)
                
                i += 1
            
            return groups
        
        def count_groups_of_size(size):
            """Count how many alternating groups have the given size."""
            groups = get_alternating_groups()
            return sum(1 for g in groups if g == size)
        
        # Process queries
        for query in queries:
            if query[0] == 1:
                # Type 1: count alternating groups of size query[1]
                size = query[1]
                count = count_groups_of_size(size)
                result.append(count)
            else:
                # Type 2: update color at index query[1]
                index = query[1]
                new_color = query[2]
                colors[index] = new_color
        
        return result
