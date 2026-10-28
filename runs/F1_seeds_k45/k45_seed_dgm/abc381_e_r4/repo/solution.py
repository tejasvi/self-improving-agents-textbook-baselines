def solve_query(substring):
    """
    Find the maximum length of a subsequence that is an 11/22 string.
    11/22 string has pattern: 1^k / 2^k for some k >= 0
    Length is 2*k + 1
    """
    n = len(substring)
    
    if n == 0:
        return 0
    
    # dp[k][phase] where:
    # phase 0: we've selected k ones and are looking for a slash
    # phase 1: we've selected k ones, a slash, and looking for m twos where m <= k
    # We track: for each k, what's the minimum position where we can have selected k ones
    #           and for each (k, m), what's the minimum position where we can have k ones, slash, m twos
    
    max_length = 0
    
    # For each possible number of 1's before slash
    for num_ones in range(n + 1):
        # Find if we can select num_ones 1's and then a slash
        ones_count = 0
        slash_pos = -1
        
        for i in range(n):
            if substring[i] == '1':
                ones_count += 1
                if ones_count == num_ones:
                    # We have num_ones 1's, now look for slash
                    for j in range(i + 1, n):
                        if substring[j] == '/':
                            slash_pos = j
                            break
                    break
        
        if slash_pos == -1:
            continue
        
        # Now we have num_ones 1's and a slash at slash_pos
        # Count how many 2's we can get after slash_pos
        twos_count = 0
        for i in range(slash_pos + 1, n):
            if substring[i] == '2':
                twos_count += 1
        
        # We can use min(num_ones, twos_count) pairs of ones and twos
        num_pairs = min(num_ones, twos_count)
        length = 2 * num_pairs + 1
        max_length = max(max_length, length)
    
    # Also check if we can just use a slash without any 1's or 2's
    for i in range(n):
        if substring[i] == '/':
            max_length = max(max_length, 1)
            break
    
    return max_length


def main():
    N, Q = map(int, input().split())
    S = input().strip()
    
    for _ in range(Q):
        L, R = map(int, input().split())
        # Convert to 0-indexed
        substring = S[L-1:R]
        result = solve_query(substring)
        print(result)


if __name__ == "__main__":
    main()
