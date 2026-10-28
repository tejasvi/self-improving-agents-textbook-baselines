from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        # Track results
        max_length = 0
        min_nodes = 1  # At minimum, a single node path
        
        def dfs(node, parent):
            nonlocal max_length, min_nodes
            
            # Dictionary: value -> (length, node_count) of best path ending at current node with that value
            # This tracks paths coming from ancestors
            paths = {nums[node]: (0, 1)}
            
            for child, edge_length in graph[node]:
                if child == parent:
                    continue
                
                child_paths = dfs(child, node)
                
                # For each path ending at child, try to extend it to current node
                new_paths = {}
                
                for val, (length, count) in child_paths.items():
                    if val not in paths:
                        # Can extend this path through current node
                        new_length = length + edge_length
                        new_count = count + 1
                        
                        if new_length > max_length or (new_length == max_length and new_count < min_nodes):
                            if new_length > max_length:
                                max_length = new_length
                                min_nodes = new_count
                            else:
                                min_nodes = min(min_nodes, new_count)
                        
                        # Add this extended path with current node's value
                        key = nums[node]
                        if key not in new_paths:
                            new_paths[key] = (new_length, new_count)
                        else:
                            # Keep the one with longer length, or fewer nodes if same length
                            old_length, old_count = new_paths[key]
                            if new_length > old_length or (new_length == old_length and new_count < old_count):
                                new_paths[key] = (new_length, new_count)
                
                # Merge new_paths into paths
                for key, (length, count) in new_paths.items():
                    if key not in paths or length > paths[key][0] or (length == paths[key][0] and count < paths[key][1]):
                        paths[key] = (length, count)
            
            return paths
        
        dfs(0, -1)
        
        return [max_length, min_nodes]
