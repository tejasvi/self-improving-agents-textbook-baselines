# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    first_line = input().split()
    N = int(first_line[0])
    T = first_line[1]
    
    strings = []
    for _ in range(N):
        strings.append(input().strip())
    
    target_len = len(T)
    
    # Precompute for each string S_i:
    # prefix_match[i][k] = how many chars of T[k:] can be matched as subsequence in S_i
    # Also compute: for string S_i and starting position k in T,
    # what is the furthest position in T we can reach?
    
    # For efficiency, compute:
    # reach[i][k] = the position in T we can reach if we start from position k in T
    #               and try to match T[k:] as a subsequence in S_i
    
    reach = []
    for i in range(N):
        s = strings[i]
        s_reach = [0] * (target_len + 1)
        
        # For each starting position k in T
        for k in range(target_len + 1):
            pos = k
            for char in s:
                if pos < target_len and char == T[pos]:
                    pos += 1
            s_reach[k] = pos
        
        reach.append(s_reach)
    
    count = 0
    # For each pair (i, j)
    for i in range(N):
        for j in range(N):
            # We match some prefix of T in S_i, and continue matching in S_j
            # After matching in S_i, we can reach reach[i][0]
            # Then in S_j, starting from that position, we can reach reach[j][reach[i][0]]
            final_pos = reach[j][reach[i][0]]
            
            if final_pos == target_len:
                count += 1
    
    print(count)

solve()
