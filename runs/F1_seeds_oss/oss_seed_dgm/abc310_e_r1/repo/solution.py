# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    # First token N (may be unused), second token S
    # Ensure we have at least two tokens
    if len(data) == 1:
        # Only string provided
        S = data[0]
    else:
        # N may be present
        S = data[1]
    dp0 = 0  # number of subarrays ending at previous position with result 0
    dp1 = 0  # number with result 1
    ans = 0
    for ch in S:
        if ch == '0':
            # new subarrays ending here
            new_dp0 = 1            # the subarray consisting of only this '0'
            new_dp1 = dp0 + dp1    # all previous subarrays become 1, none become 0
        else:  # ch == '1'
            new_dp0 = dp1          # only previous ones with result 1 become 0
            new_dp1 = dp0 + 1      # previous zeros become 1, plus the length‑1 subarray "1"
        dp0, dp1 = new_dp0, new_dp1
        ans += dp0 + dp1
    print(ans)

if __name__ == "__main__":
    solve()
