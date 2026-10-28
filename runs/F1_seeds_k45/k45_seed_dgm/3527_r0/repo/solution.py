from typing import List

class Solution:
    def numberOfAlternatingGroups(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        result = []
        
        # Helper function to compute all alternating group lengths
        def compute_group_lengths():
            # Returns a list of alternating group lengths
            lengths = []
            
            if n == 0:
                return lengths
            
            # Find the first position where a transition happens (colors[i] == colors[i+1])
            start = 0
            found_break = False
            for i in range(n):
                if colors[i] == colors[(i + 1) % n]:
                    start = (i + 1) % n
                    found_break = True
                    break
            
            # If no break found, the entire array is alternating
            if not found_break:
                lengths.append(n)
                return lengths
            
            # Otherwise, extract groups starting from the first break position
            current_length = 1
            for i in range(1, n):
                curr_idx = (start + i) % n
                prev_idx = (start + i - 1) % n
                
                if colors[curr_idx] != colors[prev_idx]:
                    current_length += 1
                else:
                    if current_length > 0:
                        lengths.append(current_length)
                    current_length = 1
            
            # Add the last group
            if current_length > 0:
                lengths.append(current_length)
            
            return lengths
        
        # Process each query
        for query in queries:
            if query[0] == 1:
                # Type 1: Count alternating groups with size query[1]
                size = query[1]
                group_lengths = compute_group_lengths()
                count = sum(1 for length in group_lengths if length == size)
                result.append(count)
            else:
                # Type 2: Update color at index query[1] to query[2]
                colors[query[1]] = query[2]
        
        return result
