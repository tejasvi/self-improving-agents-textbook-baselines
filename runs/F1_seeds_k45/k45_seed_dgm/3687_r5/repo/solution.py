from typing import List
from collections import defaultdict

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list for the tree
        graph = defaultdict(list)
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        # Track the longest path length and minimum nodes count
        max_length = 0
        min_nodes = float('inf')
        
        # DFS to find all special paths starting from each node
        def dfs(node, parent, path_length, path_nodes, used_values):
            nonlocal max_length, min_nodes
            
            # Update result if current path is valid
            if path_length > max_length:
                max_length = path_length
                min_nodes = path_nodes
            elif path_length == max_length:
                min_nodes = min(min_nodes, path_nodes)
            
            # Try to extend the path to children
            for child, edge_length in graph[node]:
                if child == parent:
                    continue
                
                child_value = nums[child]
                
                # If child value not already used, we can extend the path
                if child_value not in used_values:
                    used_values.add(child_value)
                    dfs(child, node, path_length + edge_length, path_nodes + 1, used_values)
                    used_values.remove(child_value)
        
        # Start DFS from each node as a potential starting point
        for start_node in range(n):
            used_values = {nums[start_node]}
            dfs(start_node, -1, 0, 1, used_values)
        
        return [max_length, min_nodes]
