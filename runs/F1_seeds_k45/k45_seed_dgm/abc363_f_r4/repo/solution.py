def is_palindrome(s):
    """Check if string s is a palindrome"""
    return s == s[::-1]

def has_no_zeros(s):
    """Check if string s contains no zeros"""
    return '0' not in s

def get_digits_only(s):
    """Extract only digits from a string (used for checking if number is palindrome)"""
    return ''.join(c for c in s if c.isdigit())

def is_valid_palindrome_number(n):
    """Check if n as a string is a palindrome and contains no zeros"""
    s = str(n)
    return is_palindrome(s) and has_no_zeros(s)

def factorize(n):
    """Get all divisors of n"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

def solve(n):
    # First, check if N itself is a valid palindrome
    if is_valid_palindrome_number(n):
        return str(n)
    
    # Try to find palindromic factorization expressions
    # Strategy: a * b * a where a and b are such that a*b*a = n
    # This means b = n / (a*a)
    
    divisors = factorize(n)
    
    # Try simple form: a * b * a
    for a in divisors:
        if n % (a * a) == 0:
            b = n // (a * a)
            # Check if a and b have no zeros
            a_str = str(a)
            b_str = str(b)
            if has_no_zeros(a_str) and has_no_zeros(b_str):
                result = a_str + "*" + b_str + "*" + a_str
                if is_palindrome(result):
                    return result
    
    # Try form: a * b * c * b * a
    # This means c = n / (a*a*b*b)
    for a in divisors:
        if n % (a * a) == 0:
            remainder = n // (a * a)
            sub_divisors = factorize(remainder)
            for b in sub_divisors:
                if remainder % (b * b) == 0:
                    c = remainder // (b * b)
                    a_str = str(a)
                    b_str = str(b)
                    c_str = str(c)
                    if has_no_zeros(a_str) and has_no_zeros(b_str) and has_no_zeros(c_str):
                        result = a_str + "*" + b_str + "*" + c_str + "*" + b_str + "*" + a_str
                        if is_palindrome(result):
                            return result
    
    # Try more complex patterns: a * b * c * d * c * b * a
    for a in divisors:
        if n % (a * a) > 0:
            continue
        remainder1 = n // (a * a)
        sub_divisors1 = factorize(remainder1)
        
        for b in sub_divisors1:
            if remainder1 % (b * b) > 0:
                continue
            remainder2 = remainder1 // (b * b)
            sub_divisors2 = factorize(remainder2)
            
            for c in sub_divisors2:
                if remainder2 % (c * c) > 0:
                    continue
                d = remainder2 // (c * c)
                
                a_str = str(a)
                b_str = str(b)
                c_str = str(c)
                d_str = str(d)
                
                if all(has_no_zeros(s) for s in [a_str, b_str, c_str, d_str]):
                    result = a_str + "*" + b_str + "*" + c_str + "*" + d_str + "*" + c_str + "*" + b_str + "*" + a_str
                    if is_palindrome(result):
                        return result
    
    return "-1"

# Read input
n = int(input().strip())
print(solve(n))
