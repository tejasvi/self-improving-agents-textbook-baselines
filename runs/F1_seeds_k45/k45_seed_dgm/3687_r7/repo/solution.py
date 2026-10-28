from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        """
        Find the longest special path in a tree where all node values are unique.
        
        A special path is a downward path from ancestor to descendant with unique values.
        
        Returns:
            [max_length, min_nodes] where:
            - max_length is the length of the longest special path
            - min_nodes is the minimum number of nodes in all longest special paths
        """
        n = len(nums)
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        max_length = 0
        min_nodes = float('inf')
        
        def dfs(node, parent, path_values, path_length, path_nodes):
            """
            DFS to explore all downward paths.
            
            Args:
                node: current node
                parent: parent node (to avoid going backwards in tree)
                path_values: set of unique values on current path
                path_length: total length from root to current node
                path_nodes: number of nodes from root to current node
            """
            nonlocal max_length, min_nodes
            
            # Current node's value
            curr_value = nums[node]
            
            # Check if we can extend the path (value not already in path)
            if curr_value not in path_values:
                # Add current node to path
                path_values.add(curr_value)
                
                # Update max length and min nodes
                # A path is "valid" if it has at least one node
                if path_length > max_length:
                    max_length = path_length
                    min_nodes = path_nodes
                elif path_length == max_length:
                    min_nodes = min(min_nodes, path_nodes)
                
                # Continue DFS to children
                for child, edge_length in graph[node]:
                    if child != parent:
                        dfs(child, node, path_values, path_length + edge_length, path_nodes + 1)
                
                # Backtrack
                path_values.remove(curr_value)
            else:
                # Value already in path, cannot extend further
                # But we can still explore other branches from here
                # Actually, in a special path, once a value repeats, we stop
                # So we don't continue from this node
                pass
        
        # Start DFS from root (node 0) with empty path
        dfs(0, -1, set(), 0, 1)
        
        # Handle the case where max_length is 0 (single nodes)
        if max_length == 0:
            min_nodes = 1
        
        return [max_length, min_nodes]
