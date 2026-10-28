from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        """
        Find the longest special path in a tree where all node values are unique.
        
        Args:
            edges: List of [u, v, length] representing edges in the tree
            nums: List of values at each node
        
        Returns:
            [length of longest special path, minimum nodes in longest paths]
        """
        n = len(nums)
        
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        
        # Track results
        max_length = 0
        min_nodes = 1  # Single node path has length 0
        
        # DFS to find all special paths
        # For each node, we maintain a dict mapping value -> (max_length, min_nodes)
        # of paths ending at that node with that value at the start
        
        def dfs(node, parent):
            nonlocal max_length, min_nodes
            
            # paths[value] = (length, nodes_count) for paths ending at node starting with value
            # None key represents paths that can't be extended (will start fresh from node)
            paths = {}
            
            # Single node path
            paths[nums[node]] = (0, 1)
            
            # Process each child
            for child, edge_length in adj[node]:
                if child == parent:
                    continue
                
                child_paths = dfs(child, node)
                
                # Extend existing paths with new edge
                new_paths = {}
                for value, (length, nodes) in child_paths.items():
                    if value not in paths:
                        # Can extend this path
                        new_paths[value] = (length + edge_length, nodes + 1)
                    # If value is in paths, we can't extend (would duplicate)
                
                # Merge new paths
                for value, (length, nodes) in new_paths.items():
                    if value not in paths:
                        paths[value] = (length, nodes)
                    else:
                        existing_length, existing_nodes = paths[value]
                        if length > existing_length:
                            paths[value] = (length, nodes)
                        elif length == existing_length and nodes < existing_nodes:
                            paths[value] = (length, nodes)
            
            # Update global max
            for value, (length, nodes) in paths.items():
                if length > max_length:
                    max_length = length
                    min_nodes = nodes
                elif length == max_length and nodes < min_nodes:
                    min_nodes = nodes
            
            return paths
        
        dfs(0, -1)
        
        return [max_length, min_nodes]
