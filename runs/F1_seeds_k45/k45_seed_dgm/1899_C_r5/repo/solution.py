# Write your solution here. Read from stdin, write to stdout.

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp_odd: max sum ending at current index where current element is odd
        # dp_even: max sum ending at current index where current element is even
        dp_odd = float('-inf')
        dp_even = float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(n):
            new_dp_odd = float('-inf')
            new_dp_even = float('-inf')
            
            if a[i] % 2 == 1:  # a[i] is odd
                # Start new subarray with just a[i]
                new_dp_odd = a[i]
                # Or extend from even
                if dp_even != float('-inf'):
                    new_dp_odd = max(new_dp_odd, dp_even + a[i])
            else:  # a[i] is even
                # Start new subarray with just a[i]
                new_dp_even = a[i]
                # Or extend from odd
                if dp_odd != float('-inf'):
                    new_dp_even = max(new_dp_even, dp_odd + a[i])
            
            dp_odd = new_dp_odd if new_dp_odd != float('-inf') else dp_odd
            dp_even = new_dp_even if new_dp_even != float('-inf') else dp_even
            
            # Update max sum
            if dp_odd != float('-inf'):
                max_sum = max(max_sum, dp_odd)
            if dp_even != float('-inf'):
                max_sum = max(max_sum, dp_even)
        
        print(max_sum)

solve()
