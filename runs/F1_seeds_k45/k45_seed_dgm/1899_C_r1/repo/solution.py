# Write your solution here. Read from stdin, write to stdout.

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp[i] = maximum sum of alternating parity subarray ending at index i
        max_sum = a[0]
        current_sum = a[0]
        
        for i in range(1, n):
            # Check if current element has different parity than previous
            if (a[i] % 2) != (a[i-1] % 2):
                # Different parity, we can extend the subarray
                current_sum = current_sum + a[i]
            else:
                # Same parity, start a new subarray from current element
                current_sum = a[i]
            
            max_sum = max(max_sum, current_sum)
        
        print(max_sum)

solve()
