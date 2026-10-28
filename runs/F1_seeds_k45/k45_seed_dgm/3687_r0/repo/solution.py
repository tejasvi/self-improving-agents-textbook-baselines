from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        # Track the longest path length and minimum nodes for that length
        max_length = 0
        min_nodes = float('inf')
        
        # DFS from each node
        def dfs(node, parent, current_length, current_nodes, seen_values):
            nonlocal max_length, min_nodes
            
            # Update the best result (single node path)
            if current_length > max_length:
                max_length = current_length
                min_nodes = current_nodes
            elif current_length == max_length:
                min_nodes = min(min_nodes, current_nodes)
            
            # Try to extend the path to children
            for child, edge_length in graph[node]:
                if child == parent:
                    continue
                
                # Only continue if the child's value hasn't been seen
                if nums[child] not in seen_values:
                    seen_values.add(nums[child])
                    dfs(child, node, current_length + edge_length, current_nodes + 1, seen_values)
                    seen_values.remove(nums[child])
        
        # Start DFS from each node
        for start_node in range(n):
            seen_values = {nums[start_node]}
            dfs(start_node, -1, 0, 1, seen_values)
        
        return [max_length, min_nodes]
