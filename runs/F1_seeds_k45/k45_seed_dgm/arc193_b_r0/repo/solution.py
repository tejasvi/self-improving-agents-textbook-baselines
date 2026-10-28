def solve():
    MOD = 998244353
    
    N = int(input())
    s = input().strip()
    
    # Count edges to center vertex N
    spoke_count = sum(1 for c in s if c == '1')
    
    # Generate all possible in-degree sequences
    possible_sequences = set()
    
    # We have N cycle edges and spoke_count spoke edges
    # Total edges = N + spoke_count
    # Total in-degrees = N + spoke_count
    
    # Enumerate all orientations of cycle edges
    for cycle_mask in range(1 << N):
        # For this cycle orientation, compute in-degrees from cycle
        # Bit i = 1 means edge (i, (i+1)%N) is oriented i -> (i+1)%N
        # Bit i = 0 means edge (i, (i+1)%N) is oriented (i+1)%N -> i
        
        cycle_indegrees = [0] * (N + 1)
        for i in range(N):
            if (cycle_mask >> i) & 1:
                # Edge i -> (i+1)%N
                cycle_indegrees[(i + 1) % N] += 1
            else:
                # Edge (i+1)%N -> i
                cycle_indegrees[i] += 1
        
        # Now enumerate all orientations of spoke edges
        for spoke_mask in range(1 << spoke_count):
            indegrees = cycle_indegrees[:]
            spoke_idx = 0
            for i in range(N):
                if s[i] == '1':
                    if (spoke_mask >> spoke_idx) & 1:
                        # Edge i -> N
                        indegrees[N] += 1
                    else:
                        # Edge N -> i
                        indegrees[i] += 1
                    spoke_idx += 1
            
            possible_sequences.add(tuple(indegrees))
    
    return len(possible_sequences) % MOD

print(solve())
