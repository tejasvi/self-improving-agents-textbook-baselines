class Solution:
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int:
        """
        Maximize the sum of player ids when passing a ball k times.
        
        Strategy:
        1. For each starting player, we need to compute the sum after k passes
        2. Since k can be up to 10^10, we can't simulate directly
        3. Use binary lifting: precompute jumps to 2^i positions and their sums
        4. Follow the chain and detect cycles
        5. For each starting position, use binary representation of k to jump efficiently
        """
        n = len(receiver)
        max_value = 0
        
        # For each starting player
        for start in range(n):
            # Build the chain and compute cumulative sums using binary lifting
            # We'll track: where we end up after 2^i jumps, and the sum of ids visited
            
            current = start
            total_sum = start
            remaining_k = k
            
            # We'll use a lazy approach: compute the chain up to either k passes
            # or until we detect a cycle
            visited = {}  # position -> (pass_number, cumulative_sum_so_far)
            pass_num = 0
            chain_sum = 0  # sum of visited nodes (excluding start)
            
            # Build the path until we either reach k passes or detect a cycle
            path = [start]
            path_sums = [0]  # cumulative sum at each step (excluding start)
            
            while pass_num < k:
                current = receiver[current]
                pass_num += 1
                chain_sum += current
                path.append(current)
                path_sums.append(chain_sum)
                
                # Check if we've seen this position before (cycle detection)
                if current in visited:
                    cycle_start_pass = visited[current]
                    cycle_length = pass_num - cycle_start_pass
                    
                    # We've detected a cycle
                    # sum_before_cycle = path_sums[cycle_start_pass]
                    # sum_in_one_cycle = path_sums[pass_num] - path_sums[cycle_start_pass]
                    
                    remaining_passes = k - cycle_start_pass
                    cycle_sum = path_sums[pass_num] - path_sums[cycle_start_pass]
                    
                    # How many complete cycles can we fit?
                    num_complete_cycles = remaining_passes // cycle_length
                    leftover_passes = remaining_passes % cycle_length
                    
                    # Total sum = start + sum_before_cycle + complete_cycles * cycle_sum + sum_of_leftover
                    total_before_cycle = path_sums[cycle_start_pass]
                    total_after_cycles = num_complete_cycles * cycle_sum
                    total_leftover = path_sums[cycle_start_pass + leftover_passes] - total_before_cycle
                    
                    total_sum = start + total_before_cycle + total_after_cycles + total_leftover
                    break
                
                visited[current] = pass_num
                
                if pass_num >= k:
                    total_sum = start + chain_sum
                    break
            
            max_value = max(max_value, total_sum)
        
        return max_value
