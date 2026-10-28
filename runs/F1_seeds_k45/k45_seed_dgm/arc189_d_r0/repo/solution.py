def solve(N, A):
    results = []
    
    for K in range(N):
        # For each starting position K
        max_size = find_max_size(A, K)
        results.append(max_size)
    
    return results


def find_max_size(A, K):
    """
    Find the maximum size Takahashi can achieve starting at position K.
    A: list of slime sizes
    K: starting position (0-indexed)
    """
    memo = {}
    
    def dfs(slimes_tuple, pos, takahashi_size):
        """
        slimes_tuple: tuple of remaining slime sizes (without takahashi)
        pos: position where takahashi is (index in slimes_tuple if we insert him)
        takahashi_size: current size of takahashi
        """
        key = (slimes_tuple, pos, takahashi_size)
        if key in memo:
            return memo[key]
        
        result = takahashi_size
        slimes_list = list(slimes_tuple)
        
        # Try absorbing left neighbor
        if pos > 0 and slimes_list[pos - 1] < takahashi_size:
            absorbed_size = slimes_list[pos - 1]
            new_slimes = slimes_list[:pos-1] + slimes_list[pos:]
            new_pos = pos - 1
            new_size = takahashi_size + absorbed_size
            result = max(result, dfs(tuple(new_slimes), new_pos, new_size))
        
        # Try absorbing right neighbor
        if pos < len(slimes_list) and slimes_list[pos] < takahashi_size:
            absorbed_size = slimes_list[pos]
            new_slimes = slimes_list[:pos] + slimes_list[pos+1:]
            new_pos = pos
            new_size = takahashi_size + absorbed_size
            result = max(result, dfs(tuple(new_slimes), new_pos, new_size))
        
        memo[key] = result
        return result
    
    # Remove the starting slime from the list
    remaining_slimes = list(A)
    takahashi_size = remaining_slimes[K]
    remaining_slimes.pop(K)
    
    return dfs(tuple(remaining_slimes), K, takahashi_size)


if __name__ == "__main__":
    N = int(input())
    A = list(map(int, input().split()))
    
    results = solve(N, A)
    print(' '.join(map(str, results)))
