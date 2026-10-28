MOD = 998244353

def is_good_string(s):
    """Check if a string s is a good string"""
    if len(s) == 0:
        return False
    
    a = s.count('A')
    b = s.count('B')
    c = s.count('C')
    
    # A string is good if all characters have the same parity
    # This allows us to find a z in [0, min(a,b,c)] such that
    # a-z, b-z, c-z are all even
    return a % 2 == b % 2 == c % 2

def count_good_substrings(s):
    """Count the number of good substrings in s"""
    count = 0
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_good_string(substring):
                count += 1
    return count

def solve():
    # Read input
    line1 = input().split()
    N = int(line1[0])
    K = int(line1[1])
    S = input().strip()
    
    # Find positions of '?'
    question_positions = [i for i in range(N) if S[i] == '?']
    num_questions = len(question_positions)
    
    # If no questions, just check the string
    if num_questions == 0:
        good_count = count_good_substrings(S)
        if good_count >= K:
            return 1
        else:
            return 0
    
    # Try all 3^num_questions replacements
    result = 0
    for mask in range(3 ** num_questions):
        # Create the string for this replacement
        string_list = list(S)
        temp_mask = mask
        for pos in question_positions:
            replacement = ['A', 'B', 'C'][temp_mask % 3]
            string_list[pos] = replacement
            temp_mask //= 3
        
        candidate_string = ''.join(string_list)
        
        # Count good substrings
        good_count = count_good_substrings(candidate_string)
        
        if good_count >= K:
            result += 1
    
    return result % MOD

print(solve())
