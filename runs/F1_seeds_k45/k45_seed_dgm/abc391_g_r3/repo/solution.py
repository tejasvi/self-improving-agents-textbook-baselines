#!/usr/bin/env python3
from collections import defaultdict

MOD = 998244353

def solve():
    N, M = map(int, input().split())
    S = input().strip()
    
    # dp[state] = count of strings of length up to current position that lead to this state
    # state = tuple representing the DP table row for LCS
    # For position i in the target string, we need to track the LCS DP row
    
    # lcs_dp[j] = longest common subsequence length when we've processed i chars of target
    # and j chars of source S
    
    # We'll use DP where:
    # dp[i][state] = number of strings of length i that lead to state 'state'
    # state is represented as a tuple of LCS lengths for each position in S
    
    def lcs_row(prev_row, char):
        """
        Given previous DP row and a new character, compute new DP row.
        prev_row[j] = LCS length of first i-1 chars of T with first j chars of S
        char = the i-th character of T
        Returns new_row[j] = LCS length of first i chars of T with first j chars of S
        """
        new_row = [prev_row[0]]  # LCS of char with empty string is 0
        for j in range(1, len(S) + 1):
            if char == S[j-1]:
                new_row.append(prev_row[j-1] + 1)
            else:
                new_row.append(max(new_row[j-1], prev_row[j]))
        return tuple(new_row)
    
    # Start with empty target string
    # Initial state: all zeros (LCS of empty string with any prefix of S is 0)
    current_dp = defaultdict(int)
    current_dp[tuple([0] * (N + 1))] = 1
    
    # Process each position in target string (length M)
    for i in range(M):
        next_dp = defaultdict(int)
        for state, count in current_dp.items():
            # Try adding each character 'a' to 'z'
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_state = lcs_row(state, c)
                next_dp[new_state] = (next_dp[new_state] + count) % MOD
        current_dp = next_dp
    
    # Count results by final LCS length
    result = [0] * (N + 1)
    for state, count in current_dp.items():
        lcs_length = state[-1]  # Last element is LCS with full S
        result[lcs_length] = (result[lcs_length] + count) % MOD
    
    print(' '.join(map(str, result)))

solve()
