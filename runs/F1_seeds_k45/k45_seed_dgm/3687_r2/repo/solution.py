from typing import List

class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        """
        Find the longest special path in a tree where all node values are unique.
        
        A special path is a downward path from ancestor to descendant where all
        node values in the path are unique.
        
        Returns: [length_of_longest_path, min_nodes_in_all_longest_paths]
        """
        n = len(nums)
        
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for u, v, length in edges:
            graph[u].append((v, length))
            graph[v].append((u, length))
        
        # Track the longest path found and the minimum number of nodes for that length
        max_length = 0
        min_nodes = float('inf')
        
        def dfs(node, parent, path_lengths, node_counts, last_value_set):
            """
            DFS to find all special paths in the tree.
            
            node: current node
            parent: parent node (to avoid going back)
            path_lengths: dict mapping value_set to the length of the path ending at this node
            node_counts: dict mapping value_set to the number of nodes in the path
            last_value_set: the set of values we've seen so far in current path
            """
            nonlocal max_length, min_nodes
            
            current_value = nums[node]
            
            # Try extending existing paths that don't contain the current value
            new_path_lengths = {}
            new_node_counts = {}
            
            for prev_set, prev_length in path_lengths.items():
                if current_value not in prev_set:
                    # Can extend this path
                    new_set = prev_set | {current_value}
                    new_length = prev_length + path_lengths[prev_set]
                    new_count = node_counts[prev_set] + 1
                    
                    if new_set not in new_path_lengths or new_path_lengths[new_set] < new_length:
                        new_path_lengths[new_set] = new_length
                        new_node_counts[new_set] = new_count
                    elif new_path_lengths[new_set] == new_length and new_node_counts[new_set] > new_count:
                        new_node_counts[new_set] = new_count
            
            # Also consider starting a new path from this node
            new_path_lengths[frozenset({current_value})] = 0
            new_node_counts[frozenset({current_value})] = 1
            
            # Update the global maximum and minimum nodes
            for value_set, length in new_path_lengths.items():
                if length > max_length:
                    max_length = length
                    min_nodes = new_node_counts[value_set]
                elif length == max_length:
                    min_nodes = min(min_nodes, new_node_counts[value_set])
            
            # Continue DFS to children
            for child, edge_length in graph[node]:
                if child != parent:
                    # Prepare path_lengths for the child
                    child_path_lengths = {}
                    child_node_counts = {}
                    
                    for value_set, length in new_path_lengths.items():
                        if current_value not in value_set or len(value_set) == 0:
                            child_path_lengths[value_set] = length + edge_length
                            child_node_counts[value_set] = new_node_counts[value_set]
                    
                    dfs(child, node, child_path_lengths, child_node_counts, last_value_set)
        
        # Start DFS from root node 0
        dfs(0, -1, {}, {}, frozenset())
        
        # Handle edge case where max_length is 0 (no edges in special paths)
        if min_nodes == float('inf'):
            min_nodes = 1
        
        return [max_length, min_nodes]
