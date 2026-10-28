from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        
        # Build adjacency list (tree)
        adj = [[] for _ in range(n)]
        for u, v, length in edges:
            adj[u].append((v, length))
            adj[v].append((u, length))
        
        max_length = 0
        min_nodes_count = 1  # At minimum, a single node path
        
        def dfs(node, parent):
            nonlocal max_length, min_nodes_count
            
            # paths_dict: maps frozenset of values -> (max_length, min_node_count)
            # This tracks all possible paths ending at this node
            # Keys are sets of values in the path, values are (length, node_count) tuples
            paths_dict = {}
            
            # Add path starting from this node (just the node itself)
            node_val = nums[node]
            paths_dict[frozenset([node_val])] = (0, 1)
            
            # Process children
            for child, edge_length in adj[node]:
                if child == parent:
                    continue
                
                child_val = nums[child]
                child_paths = dfs(child, node)
                
                # For each path from child, try to extend it to current node
                for values_set, (child_length, child_nodes) in child_paths.items():
                    # Check if we can extend: child path should not contain current node's value
                    if node_val not in values_set:
                        # New path: current node -> child path
                        new_length = edge_length + child_length
                        new_nodes = 1 + child_nodes
                        new_values = frozenset([node_val]) | values_set
                        
                        # Update or add this path in paths_dict
                        if new_values not in paths_dict:
                            paths_dict[new_values] = (new_length, new_nodes)
                        else:
                            curr_length, curr_nodes = paths_dict[new_values]
                            if new_length > curr_length:
                                paths_dict[new_values] = (new_length, new_nodes)
                            elif new_length == curr_length and new_nodes < curr_nodes:
                                paths_dict[new_values] = (new_length, new_nodes)
            
            # Update global max with all paths from this node
            for values_set, (path_length, path_nodes) in paths_dict.items():
                if path_length > max_length:
                    max_length = path_length
                    min_nodes_count = path_nodes
                elif path_length == max_length and path_nodes < min_nodes_count:
                    min_nodes_count = path_nodes
            
            return paths_dict
        
        dfs(0, -1)
        return [max_length, min_nodes_count]
