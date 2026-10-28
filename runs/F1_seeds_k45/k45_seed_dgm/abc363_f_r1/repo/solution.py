def is_palindrome(s):
    """Check if string is a palindrome"""
    return s == s[::-1]

def has_only_valid_digits(s):
    """Check if string contains only digits 1-9"""
    return all(c in '123456789' for c in s)

def find_palindromic_expression(N):
    """Try to find a palindromic expression that evaluates to N"""
    
    # Case 1: Check if N itself is a palindrome with valid digits
    s = str(N)
    if is_palindrome(s) and has_only_valid_digits(s):
        return s
    
    # Case 2: Try to construct palindromic expressions with multiplications
    # Strategy: Find factor pairs and try to construct a*b*a form
    
    # Try simple forms like a*N/a where a divides N
    # For a*N/a to be a palindrome, we need a and N/a to form a palindrome
    
    # Check divisors up to sqrt(N)
    divisors = []
    i = 1
    while i * i <= N:
        if N % i == 0:
            divisors.append(i)
            if i != N // i:
                divisors.append(N // i)
        i += 1
    
    divisors.sort()
    
    # Try patterns like: a*b*a where a*b*a = N
    # This means a^2 * b = N, so b = N / a^2
    for a in divisors:
        if a * a > N:
            break
        if N % (a * a) == 0:
            b = N // (a * a)
            s_a = str(a)
            s_b = str(b)
            # Check if a and b have only valid digits
            if has_only_valid_digits(s_a) and has_only_valid_digits(s_b):
                # Try a*b*a pattern
                expr = s_a + '*' + s_b + '*' + s_a
                if is_palindrome(expr):
                    return expr
    
    # Try patterns like: a*b*c*b*a where a*b*c*b*a = N
    # This means a^2 * b^2 * c = N
    for a in divisors:
        if a * a > N:
            break
        if N % (a * a) == 0:
            remaining = N // (a * a)
            for b in divisors:
                if b * b > remaining:
                    break
                if remaining % (b * b) == 0:
                    c = remaining // (b * b)
                    s_a = str(a)
                    s_b = str(b)
                    s_c = str(c)
                    if has_only_valid_digits(s_a) and has_only_valid_digits(s_b) and has_only_valid_digits(s_c):
                        expr = s_a + '*' + s_b + '*' + s_c + '*' + s_b + '*' + s_a
                        if is_palindrome(expr):
                            return expr
    
    # Try more complex patterns with more factors
    # Try: a*b*c*d*c*b*a
    for a in divisors:
        if a * a > N:
            break
        if N % (a * a) == 0:
            remaining = N // (a * a)
            for b in divisors:
                if b * b > remaining:
                    break
                if remaining % (b * b) == 0:
                    remaining2 = remaining // (b * b)
                    for c in divisors:
                        if c * c > remaining2:
                            break
                        if remaining2 % (c * c) == 0:
                            d = remaining2 // (c * c)
                            s_a = str(a)
                            s_b = str(b)
                            s_c = str(c)
                            s_d = str(d)
                            if (has_only_valid_digits(s_a) and has_only_valid_digits(s_b) and 
                                has_only_valid_digits(s_c) and has_only_valid_digits(s_d)):
                                expr = s_a + '*' + s_b + '*' + s_c + '*' + s_d + '*' + s_c + '*' + s_b + '*' + s_a
                                if is_palindrome(expr):
                                    return expr
    
    return None

N = int(input())
result = find_palindromic_expression(N)
if result:
    print(result)
else:
    print(-1)
