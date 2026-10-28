def lcs_length(s, t):
    """Compute LCS length between s and t"""
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

def solve():
    MOD = 998244353
    N, M = map(int, input().split())
    S = input().strip()
    
    # For small M, we can use a smarter DP
    # Key idea: we need to compute for each possible string T of length M,
    # what is its LCS with S. But 26^M can be large.
    #
    # Better idea: use DP where we build T character by character
    # and track what LCS values are possible
    #
    # dp[i][k] = number of strings of length i with LCS exactly k
    # But we need an intermediate representation during construction
    #
    # The trick: LCS(S, T[0:i]) depends on the current characters of T
    # When we add a new character, we need to see how it affects the LCS
    #
    # We track: dp[i][(s_idx, t_idx, lcs_val)] = count
    # This represents: after processing i characters of T,
    # if we only considered S[0:s_idx] and T[0:t_idx],
    # we'd have LCS value lcs_val
    #
    # Actually, that's too complex. Let's use a different state:
    # dp[i][lcs_achieved] = number of strings of length i with LCS(S, T[0:i]) = lcs_achieved
    #
    # To transition from i to i+1, we try all 26 characters
    # For each character c:
    #   For each previous state with LCS value k:
    #     Compute the new LCS value when we append c to T
    #     This requires knowing the full T, but T is implicit
    #
    # The issue: to compute LCS(S, T[0:i+1]), we need to know all of T[0:i]
    # So we can't just track LCS values in a simple DP
    
    # Solution: use recursive generation with memoization
    # But with M up to 100, and 26^M possibilities, this won't work
    
    # Alternative: observe that many strings give the same LCS
    # We can compute LCS more cleverly
    
    # Key insight for LCS: we can use DP
    # dp[i][j][k] = true if LCS(S[0:i], T[0:j]) can be k
    # But we also want counts...
    
    # Actually, let's use:
    # dp[i][j][k] = number of strings of length j with LCS(S[0:i], T[0:j]) = k
    # where T is a string we're building character by character
    
    # When we extend from position j to j+1 with a new character c:
    # The LCS(S[0:i], T[0:j+1]) depends on:
    #   - Previous LCS(S[0:i], T[0:j])
    #   - Whether c matches S[i-1]
    #   - All previous values in the DP table
    
    # Let's compute the DP table more explicitly:
    
    # dp[i][j][k] = count of strings T of length i such that
    #     LCS(S[0:j], T[0:i]) = k
    
    # Base case: dp[0][j][0] = 1 for all j (empty string)
    
    # Transition: when we add character c at position i:
    #   dp[i+1][j][k] comes from:
    #   1. dp[i][j][k] if we use a character that doesn't match S[j-1]
    #   2. dp[i][j-1][k-1] if we use a character that matches S[j-1]
    #   3. dp[i][j][k] from previous (not matching S[j-1])
    
    INF = float('inf')
    
    # dp[i][j][k] = count of strings of length i where LCS(S[0:j], str) = k
    dp = [[[0] * (N + 1) for _ in range(N + 1)] for _ in range(M + 1)]
    
    # Base case: empty string has LCS 0 with all prefixes of S
    for j in range(N + 1):
        dp[0][j][0] = 1
    
    # Fill the DP table
    for i in range(M):
        for j in range(N + 1):
            for k in range(j + 1):  # LCS can't be more than min(i, j)
                if dp[i][j][k] == 0:
                    continue
                
                if j < N:
                    # Case 1: Add a character that matches S[j]
                    # This increases LCS by 1
                    dp[i + 1][j + 1][k + 1] = (dp[i + 1][j + 1][k + 1] + dp[i][j][k]) % MOD
                
                # Case 2: Add a character that doesn't match S[j]
                # (or we're past S)
                # This doesn't increase the LCS for the current j
                # But we might improve by matching a later character
                
                # Not matching S[j]: LCS stays the same
                dp[i + 1][j][k] = (dp[i + 1][j][k] + dp[i][j][k] * 25) % MOD  # 25 non-matching chars
                
                # Actually, we need to be more careful
                # When we add character c:
                # - If c == S[j], we can match it: new LCS is k+1
                # - If c != S[j], LCS stays k, but we move to considering S[j+1], S[j+2], etc.
                
                # Hmm, the state (i, j, k) means we've processed S[0:j]
                # But we might not match all of S[0:j]
                # We need to track whether we're committed to this matching or not
    
    # This is getting confused. Let me reconsider.
    
    # Cleaner approach:
    # dp[i][k] = number of strings of length i with LCS(S, T) = k
    # To compute this, we use the observation that LCS can be computed character by character
    
    # Actually, I'll use a different formulation:
    # dp[i] = dictionary mapping LCS values to counts
    # dp[i][k] = count of strings of length i with LCS(S, T) = k
    
    dp = [dict() for _ in range(M + 1)]
    dp[0][0] = 1  # Empty string has LCS 0
    
    for i in range(M):
        for lcs_val, count in dp[i].items():
            # For each of 26 characters
            for c_val in range(26):
                c = chr(ord('a') + c_val)
                
                # Try extending with this character
                # We need to compute: what's the new LCS?
                # To do this, we need to know the actual string T, which we don't have
                
                # Alternative: represent strings implicitly
                # Group strings by their LCS value
                # When we add character c, what new LCS values are possible?
                
                # A string with LCS k can become:
                # - LCS k+1 if c matches some character in S that we can use
                # - LCS k if c doesn't help
                
                # But this depends on which characters we've already used!
                pass
    
    print(" ".join(map(str, [dp[M].get(k, 0) for k in range(N + 1)])))

solve()
