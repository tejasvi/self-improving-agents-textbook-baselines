# Write your solution here. Read from stdin, write to stdout.

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        if n == 1:
            print(a[0])
            continue
        
        # dp[i] = maximum sum of valid subarray ending at position i
        dp = [0] * n
        dp[0] = a[0]
        max_sum = a[0]
        
        for i in range(1, n):
            # Check if we can extend from i-1
            # Adjacent elements must have different parities
            if (a[i] % 2) != (a[i-1] % 2):
                # Different parities, we can extend
                dp[i] = dp[i-1] + a[i]
            else:
                # Same parities, start new subarray from i
                dp[i] = a[i]
            
            max_sum = max(max_sum, dp[i])
        
        print(max_sum)

solve()
