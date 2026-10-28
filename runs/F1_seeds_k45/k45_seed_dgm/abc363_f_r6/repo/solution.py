def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]

def has_only_valid_digits(s):
    """Check if string contains only digits 1-9 (no 0)."""
    return all(c in '123456789' for c in s)

def check_no_zeros(n):
    """Check if number n contains any zeros."""
    return '0' not in str(n)

def generate_palindromes(max_val):
    """Generate all palindromic numbers up to max_val with only digits 1-9."""
    palindromes = []
    for num in range(1, min(max_val + 1, 10**7)):
        s = str(num)
        if is_palindrome(s) and has_only_valid_digits(s):
            palindromes.append(num)
    return palindromes

def solve(n):
    # First, check if N itself is a palindrome with only valid digits
    s_n = str(n)
    if is_palindrome(s_n) and has_only_valid_digits(s_n):
        return s_n
    
    # Generate small palindromes for factorization
    small_pals = generate_palindromes(100000)
    
    # Strategy 1: Try two-factor palindromes (d * q where d is a small palindrome)
    for d in small_pals:
        if d * d > n:
            break
        if n % d == 0:
            q = n // d
            if has_only_valid_digits(str(q)) and check_no_zeros(q):
                if is_palindrome(str(q)):
                    expr = str(d) + '*' + str(q)
                    if is_palindrome(expr):
                        return expr
    
    # Strategy 2: Try a*b*a structure (a^2 * b = n)
    for a in small_pals:
        if a * a * a > n:
            break
        if n % (a * a) == 0:
            b = n // (a * a)
            if has_only_valid_digits(str(b)) and check_no_zeros(b):
                if is_palindrome(str(b)):
                    expr = str(a) + '*' + str(b) + '*' + str(a)
                    if is_palindrome(expr):
                        return expr
    
    # Strategy 3: Try a*b*c*b*a (a^2 * b^2 * c = n)
    for a in small_pals:
        if a * a > n:
            break
        if n % (a * a) != 0:
            continue
        
        remainder = n // (a * a)
        
        for b in small_pals:
            if b * b > remainder:
                break
            if remainder % (b * b) == 0:
                c = remainder // (b * b)
                
                if has_only_valid_digits(str(c)) and check_no_zeros(c):
                    if is_palindrome(str(c)):
                        expr = str(a) + '*' + str(b) + '*' + str(c) + '*' + str(b) + '*' + str(a)
                        if is_palindrome(expr):
                            return expr
    
    # Strategy 4: Try a*b*c*d*c*b*a (a^2 * b^2 * c^2 * d = n)
    for a in small_pals:
        if a * a > n:
            break
        if n % (a * a) != 0:
            continue
        
        remainder = n // (a * a)
        
        for b in small_pals:
            if b * b > remainder:
                break
            if remainder % (b * b) != 0:
                continue
            
            remainder2 = remainder // (b * b)
            
            for c in small_pals:
                if c * c > remainder2:
                    break
                if remainder2 % (c * c) == 0:
                    d = remainder2 // (c * c)
                    
                    if has_only_valid_digits(str(d)) and check_no_zeros(d):
                        if is_palindrome(str(d)):
                            expr = str(a) + '*' + str(b) + '*' + str(c) + '*' + str(d) + '*' + str(c) + '*' + str(b) + '*' + str(a)
                            if is_palindrome(expr):
                                return expr
    
    return "-1"

n = int(input())
print(solve(n))
