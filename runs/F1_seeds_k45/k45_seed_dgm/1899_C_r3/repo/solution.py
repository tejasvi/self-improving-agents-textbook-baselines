# Write your solution here. Read from stdin, write to stdout.

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp[i][p] = max sum ending at position i where p is parity of a[i]
        # p = 0 for even, p = 1 for odd
        # We only need to track the previous state
        
        max_sum = float('-inf')
        
        # dp_odd = max sum ending with odd number
        # dp_even = max sum ending with even number
        dp_odd = float('-inf')
        dp_even = float('-inf')
        
        for i in range(n):
            parity = a[i] % 2
            
            if parity == 1:  # current element is odd
                # Either start new subarray or extend from even
                new_dp_odd = max(a[i], dp_even + a[i])
                dp_odd = new_dp_odd
            else:  # current element is even
                # Either start new subarray or extend from odd
                new_dp_even = max(a[i], dp_odd + a[i])
                dp_even = new_dp_even
            
            max_sum = max(max_sum, dp_odd, dp_even)
        
        print(max_sum)

solve()
