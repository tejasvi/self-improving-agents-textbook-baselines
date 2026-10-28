def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def has_no_zeros(s):
    """Check if a string doesn't contain 0"""
    return '0' not in s

def try_direct(n):
    """Try if N itself is a palindrome without zeros"""
    s = str(n)
    if has_no_zeros(s) and is_palindrome(s):
        return s
    return None

def get_all_divisors(n, limit=None):
    """Get all divisors of n up to limit"""
    divisors = []
    i = 1
    while i * i <= n:
        if limit and i > limit:
            break
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(set(divisors))

def is_valid_number(n):
    """Check if number has no zeros"""
    return has_no_zeros(str(n))

def try_construct_palindrome(n, depth=0):
    """Try to construct a palindromic expression for n using a*b*a pattern recursively"""
    if depth > 3:  # Limit recursion depth
        return None
    
    # Get divisors of n (limit search to avoid timeout)
    # For a*b*a = n, we iterate over possible values of a
    limit = int(n ** 0.5) + 1
    
    # Try divisors up to a reasonable limit
    checked = set()
    for a in range(1, min(limit + 1, 10000001)):
        if a in checked:
            continue
        checked.add(a)
        
        if not is_valid_number(a):
            continue
        
        if n % (a * a) == 0:
            b = n // (a * a)
            
            if not is_valid_number(b):
                continue
            
            s_a = str(a)
            s_b = str(b)
            
            # Check if b is a palindrome
            if is_palindrome(s_b):
                result = s_a + '*' + s_b + '*' + s_a
                if is_palindrome(result):
                    return result
            
            # Try to construct b recursively
            if depth < 2:
                b_expr = try_construct_palindrome(b, depth + 1)
                if b_expr:
                    result = s_a + '*' + b_expr + '*' + s_a
                    if is_palindrome(result):
                        return result
    
    return None

def solve(n):
    """Find a palindromic expression that evaluates to n"""
    
    # Try if n itself is a palindrome
    result = try_direct(n)
    if result:
        return result
    
    # Try a*b*a pattern with recursion
    result = try_construct_palindrome(n)
    if result:
        return result
    
    return "-1"

# Read input
n = int(input().strip())

# Solve and print result
print(solve(n))
