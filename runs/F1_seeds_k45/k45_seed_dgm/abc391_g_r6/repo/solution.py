def solve():
    MOD = 998244353
    N, M = map(int, input().split())
    S = input().strip()
    
    # dp[str_pos][lcs_row] = count of strings of length str_pos
    # where lcs_row[i] = LCS(string, S[0:i])
    # lcs_row is a tuple of length N+1
    
    dp = [{} for _ in range(M + 1)]
    
    # Initial state: empty string
    initial_row = tuple([0] * (N + 1))
    dp[0][initial_row] = 1
    
    for str_pos in range(M):
        for lcs_row, count in dp[str_pos].items():
            # Try adding each character a-z
            for c in 'abcdefghijklmnopqrstuvwxyz':
                # Compute new LCS row when adding character c
                new_row = list(lcs_row)
                for j in range(1, N + 1):
                    if S[j - 1] == c:
                        new_row[j] = new_row[j - 1] + 1
                    else:
                        new_row[j] = max(new_row[j], new_row[j - 1])
                
                new_row_tuple = tuple(new_row)
                if new_row_tuple not in dp[str_pos + 1]:
                    dp[str_pos + 1][new_row_tuple] = 0
                dp[str_pos + 1][new_row_tuple] = (dp[str_pos + 1][new_row_tuple] + count) % MOD
    
    # Count strings by final LCS length
    result = [0] * (N + 1)
    for lcs_row, count in dp[M].items():
        lcs_len = lcs_row[N]  # LCS with entire S
        result[lcs_len] = (result[lcs_len] + count) % MOD
    
    print(' '.join(map(str, result)))

solve()
