def is_palindrome(s):
    return s == s[::-1]

def num_to_string(n):
    """Convert number to string, return None if it has a 0"""
    s = str(n)
    if '0' in s:
        return None
    return s

def reverse_num(n):
    """Reverse the digits of a number"""
    s = str(n)
    reversed_s = s[::-1]
    if '0' in reversed_s:
        return None
    return int(reversed_s)

def get_divisors_up_to(n, max_val):
    """Get all divisors of n that are at most max_val"""
    divisors = set()
    i = 1
    # Only iterate up to sqrt(n) to find divisors
    while i * i <= n:
        if n % i == 0:
            if i <= max_val:
                divisors.add(i)
            # For large divisors, only add if they are <= max_val
            if i != n // i:
                large = n // i
                if large <= max_val:
                    divisors.add(large)
        i += 1
        # For efficiency, if we've found many divisors, we can continue
        if i > max_val and i * i > n:
            break
    return sorted(divisors)

def solve(n):
    # Case 1: N itself is a palindrome without zeros
    n_str = num_to_string(n)
    if n_str and is_palindrome(n_str):
        return n_str
    
    # Case 2: Try single digit * palindrome * single digit
    # Pattern: d * p * d where p is palindrome
    for d in range(1, 10):
        if n % (d * d) == 0:
            p = n // (d * d)
            p_str = num_to_string(p)
            if p_str and is_palindrome(p_str):
                return str(d) + '*' + p_str + '*' + str(d)
    
    # Case 3: Try pattern a * b * c * b * a
    # where a and b are single digits, c is palindrome
    for a in range(1, 10):
        if n % (a * a) != 0:
            continue
        n2 = n // (a * a)
        
        for b in range(1, 10):
            if n2 % (b * b) != 0:
                continue
            c = n2 // (b * b)
            c_str = num_to_string(c)
            if c_str and is_palindrome(c_str):
                return str(a) + '*' + str(b) + '*' + c_str + '*' + str(b) + '*' + str(a)
    
    # Case 4: Try pattern a * b * c * reverse(b) * a
    # where a is single digit, b and c can be multi-digit, c is palindrome
    for a in range(1, 10):
        if n % (a * a) != 0:
            continue
        n_div_aa = n // (a * a)
        
        # Get divisors up to limit
        limit = min(10**6, int(n_div_aa**0.5) + 1000)
        divisors = get_divisors_up_to(n_div_aa, limit)
        
        for b in divisors:
            b_str = num_to_string(b)
            if b_str is None:
                continue
            
            b_rev = reverse_num(b)
            if b_rev is None:
                continue
            
            if n_div_aa % (b * b_rev) != 0:
                continue
            
            c = n_div_aa // (b * b_rev)
            c_str = num_to_string(c)
            
            if c_str and is_palindrome(c_str):
                candidate = str(a) + '*' + b_str + '*' + c_str + '*' + str(b_rev) + '*' + str(a)
                if is_palindrome(candidate):
                    return candidate
    
    # Case 5: Try pattern b * c * reverse(b)
    # where b and c are multi-digit, c is palindrome
    max_limit = min(10**6, int(n**0.4) + 1000)
    divisors = get_divisors_up_to(n, max_limit)
    
    for b in divisors:
        b_str = num_to_string(b)
        if b_str is None:
            continue
        
        b_rev = reverse_num(b)
        if b_rev is None:
            continue
        
        if n % (b * b_rev) != 0:
            continue
        
        c = n // (b * b_rev)
        c_str = num_to_string(c)
        
        if c_str and is_palindrome(c_str):
            candidate = b_str + '*' + c_str + '*' + str(b_rev)
            if is_palindrome(candidate):
                return candidate
    
    return "-1"

n = int(input())
print(solve(n))
