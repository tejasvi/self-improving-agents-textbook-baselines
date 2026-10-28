#!/usr/bin/env python3
"""
Solution for the Many LCS problem.

Key insight: We build all possible strings T of length M character by character,
and track the LCS with all prefixes of S. This allows us to count how many 
strings have exactly LCS of length k with S.

Time Complexity: O(M * |states| * 26 * N) where |states| is the number of unique
LCS state configurations. In practice, |states| is much smaller than N^M.

Space Complexity: O(|states| * (N+1)) for storing the DP states.
"""
MOD = 998244353

def solve():
    N, M = map(int, input().split())
    S = input().strip()
    
    # State representation: tuple of N+1 integers
    # state[i] = LCS of current string T with S[0..i]
    # state[0] is always 0 (LCS with empty string)
    # state[N] is the final LCS value we care about
    
    # dp[m] = dictionary mapping state -> count of strings producing that state
    # where m is the current length of string T being built
    
    dp = [dict() for _ in range(M + 1)]
    
    # Base case: empty string T
    # LCS with any prefix of S is 0
    dp[0][tuple([0] * (N + 1))] = 1
    
    # Build string T character by character
    for m in range(M):
        for lcs_state, count in dp[m].items():
            # Try each character a-z
            for c_ord in range(26):
                c = chr(ord('a') + c_ord)
                
                # Compute new LCS state after appending character c
                # Use standard LCS DP recurrence:
                # If c == S[i-1]: we can extend the LCS from position i-1
                # Otherwise: we take the best we had without this character
                new_lcs = [0] * (N + 1)
                new_lcs[0] = 0
                
                for i in range(1, N + 1):
                    if c == S[i - 1]:
                        # Match: extend LCS from previous position
                        new_lcs[i] = lcs_state[i - 1] + 1
                    else:
                        # No match: best of skipping character from T or from S
                        new_lcs[i] = max(lcs_state[i], new_lcs[i - 1])
                
                new_state = tuple(new_lcs)
                
                if new_state not in dp[m + 1]:
                    dp[m + 1][new_state] = 0
                dp[m + 1][new_state] = (dp[m + 1][new_state] + count) % MOD
    
    # Count by final LCS value
    result = [0] * (N + 1)
    for lcs_state, count in dp[M].items():
        final_lcs = lcs_state[N]
        result[final_lcs] = (result[final_lcs] + count) % MOD
    
    print(' '.join(map(str, result)))

solve()
