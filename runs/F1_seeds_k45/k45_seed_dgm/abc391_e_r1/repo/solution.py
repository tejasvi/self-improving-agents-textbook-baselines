def solve():
    N = int(input())
    A = input().split()
    A = [int(x) for x in A]
    
    # dp[level][pos][bit] = minimum cost to make position pos at level have value bit
    # level 0 is the original string, level N is the final single bit
    
    # Initialize level 0 (original string)
    # dp[0][i][0] = cost to make A[i] = 0
    # dp[0][i][1] = cost to make A[i] = 1
    dp = [[{0: 0, 1: 0} for _ in range(len(A))] for _ in range(N + 1)]
    
    for i in range(len(A)):
        if A[i] == 0:
            dp[0][i][0] = 0
            dp[0][i][1] = 1
        else:
            dp[0][i][0] = 1
            dp[0][i][1] = 0
    
    # Build up the levels
    for level in range(1, N + 1):
        prev_len = len(dp[level - 1])
        new_len = prev_len // 3
        
        for i in range(new_len):
            # The three positions in the previous level that feed into position i
            pos0 = 3 * i
            pos1 = 3 * i + 1
            pos2 = 3 * i + 2
            
            # Try all 8 possible combinations of bits for the three inputs
            # To get a 0 at this position, we need at least 2 zeros
            # To get a 1 at this position, we need at least 2 ones
            
            min_cost_0 = float('inf')
            min_cost_1 = float('inf')
            
            for b0 in [0, 1]:
                for b1 in [0, 1]:
                    for b2 in [0, 1]:
                        cost = dp[level - 1][pos0][b0] + dp[level - 1][pos1][b1] + dp[level - 1][pos2][b2]
                        majority = 1 if (b0 + b1 + b2) >= 2 else 0
                        
                        if majority == 0:
                            min_cost_0 = min(min_cost_0, cost)
                        else:
                            min_cost_1 = min(min_cost_1, cost)
            
            dp[level][i][0] = min_cost_0
            dp[level][i][1] = min_cost_1
    
    # The final result is at position 0 of level N
    final_0_cost = dp[N][0][0]
    final_1_cost = dp[N][0][1]
    
    # First, compute what the original result is
    result = get_result(A)
    
    # If result is 0, we need to change to 1 (cost: final_1_cost)
    # If result is 1, we need to change to 0 (cost: final_0_cost)
    if result == 0:
        print(final_1_cost)
    else:
        print(final_0_cost)

def get_result(bits):
    """Apply majority vote operation until we get a single bit"""
    while len(bits) > 1:
        new_bits = []
        for i in range(0, len(bits), 3):
            majority = 1 if (bits[i] + bits[i+1] + bits[i+2]) >= 2 else 0
            new_bits.append(majority)
        bits = new_bits
    return bits[0]

solve()
