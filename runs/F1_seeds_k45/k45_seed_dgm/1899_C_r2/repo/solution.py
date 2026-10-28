# Write your solution here. Read from stdin, write to stdout.

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp[i] = maximum sum of valid subarray ending at index i
        # A subarray is valid if adjacent elements have alternating parities
        dp = [0] * n
        dp[0] = a[0]
        max_sum = a[0]
        
        for i in range(1, n):
            # Check if we can extend from previous position
            # Adjacent elements must have different parities
            if (a[i] % 2) != (a[i-1] % 2):
                # Different parities, can extend or start new
                dp[i] = max(a[i], dp[i-1] + a[i])
            else:
                # Same parity, must start new subarray
                dp[i] = a[i]
            
            max_sum = max(max_sum, dp[i])
        
        print(max_sum)

solve()
