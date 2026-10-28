from functools import lru_cache

MOD = 998244353

def is_good(s):
    """Check if a string can be reduced to empty using operations"""
    @lru_cache(maxsize=None)
    def can_reduce(s):
        if not s:
            return True
        
        # Try operation 1: remove two identical characters
        for i in range(len(s)):
            for j in range(i+1, len(s)):
                if s[i] == s[j]:
                    new_s = s[:i] + s[i+1:j] + s[j+1:]
                    if can_reduce(new_s):
                        return True
        
        # Try operation 2: remove one A, one B, one C
        count_a = s.count('A')
        count_b = s.count('B')
        count_c = s.count('C')
        
        if count_a > 0 and count_b > 0 and count_c > 0:
            # Find positions of A, B, C and remove them
            a_pos = s.index('A')
            b_pos = s.index('B')
            c_pos = s.index('C')
            
            positions = sorted([a_pos, b_pos, c_pos], reverse=True)
            new_s = s
            for pos in positions:
                new_s = new_s[:pos] + new_s[pos+1:]
            
            if can_reduce(new_s):
                return True
        
        return False
    
    return can_reduce(s)

def count_good_substrings(s):
    """Count the number of good substrings in s"""
    count = 0
    n = len(s)
    for i in range(n):
        for j in range(i+1, n+1):
            substring = s[i:j]
            if is_good(substring):
                count += 1
    return count

def solve():
    line = input().split()
    N = int(line[0])
    K = int(line[1])
    S = input().strip()
    
    # Count question marks
    q_count = S.count('?')
    
    # Generate all possible replacements
    result = 0
    
    def generate_and_count(index, current_string):
        nonlocal result
        
        if index == N:
            # Check if this replacement has at least K good substrings
            good_count = count_good_substrings(current_string)
            if good_count >= K:
                result += 1
                result %= MOD
            return
        
        if S[index] == '?':
            for char in ['A', 'B', 'C']:
                generate_and_count(index + 1, current_string + char)
        else:
            generate_and_count(index + 1, current_string + S[index])
    
    generate_and_count(0, "")
    print(result)

solve()
