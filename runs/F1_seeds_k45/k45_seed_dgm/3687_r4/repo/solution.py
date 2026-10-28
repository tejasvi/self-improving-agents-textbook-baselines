from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        max_length = 0
        min_nodes = float('inf')
        
        def dfs(node, parent, path_length, path_nodes, visited_values):
            """
            DFS to explore all downward paths from current node.
            
            Args:
                node: current node
                parent: parent node (to avoid going back up the tree)
                path_length: total length of path so far
                path_nodes: number of nodes in path so far
                visited_values: set of values already in the path
            """
            nonlocal max_length, min_nodes
            
            # Update result with current path (a single node counts as a path with length 0)
            if path_length > max_length:
                max_length = path_length
                min_nodes = path_nodes
            elif path_length == max_length:
                min_nodes = min(min_nodes, path_nodes)
            
            # Try to extend the path to each child
            for neighbor, edge_length in graph[node]:
                if neighbor == parent:
                    continue
                
                neighbor_value = nums[neighbor]
                
                # If the neighbor's value is not in the current path, we can extend
                if neighbor_value not in visited_values:
                    visited_values.add(neighbor_value)
                    dfs(neighbor, node, path_length + edge_length, path_nodes + 1, visited_values)
                    visited_values.remove(neighbor_value)
        
        # Start DFS from each node as a potential starting point
        for start_node in range(n):
            visited_values = {nums[start_node]}
            dfs(start_node, -1, 0, 1, visited_values)
        
        return [max_length, min_nodes]
