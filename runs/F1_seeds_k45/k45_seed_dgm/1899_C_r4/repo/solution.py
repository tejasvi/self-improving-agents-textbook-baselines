def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp[i][0] = max sum ending at i where a[i] is even
        # dp[i][1] = max sum ending at i where a[i] is odd
        
        if n == 1:
            print(a[0])
            continue
        
        # Initialize for the first element
        parity = a[0] % 2
        dp = [float('-inf')] * 2
        dp[parity] = a[0]
        
        max_sum = a[0]
        
        for i in range(1, n):
            new_dp = [float('-inf')] * 2
            curr_parity = a[i] % 2
            
            # Option 1: Start a new subarray with just a[i]
            new_dp[curr_parity] = a[i]
            
            # Option 2: Extend from previous element with different parity
            prev_parity = 1 - curr_parity
            if dp[prev_parity] != float('-inf'):
                new_dp[curr_parity] = max(new_dp[curr_parity], dp[prev_parity] + a[i])
            
            dp = new_dp
            max_sum = max(max_sum, dp[curr_parity])
        
        print(max_sum)

solve()
