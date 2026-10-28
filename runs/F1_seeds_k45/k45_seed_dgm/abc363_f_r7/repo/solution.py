import sys
sys.setrecursionlimit(10000)

def is_palindrome(s):
    return s == s[::-1]

def is_valid_number_string(s):
    """Check if string is a valid number (only digits 1-9)"""
    return s and all(c in '123456789' for c in s) and s[0] in '123456789'

def is_valid_solution(s):
    """Check if string is valid palindromic expression"""
    if not s or s[0] not in '123456789':
        return False
    if not is_palindrome(s):
        return False
    if not all(c in '123456789*' for c in s):
        return False
    return True

def evaluate_expr(s):
    """Safely evaluate the expression"""
    try:
        return eval(s)
    except:
        return None

def get_divisors(n, limit=10000):
    """Get divisors of n, limiting search for large n"""
    divisors = []
    i = 1
    while i * i <= n and i <= limit:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(set(divisors))

memo = {}

def find_palindrome_expr(n, max_depth=10, depth=0):
    """
    Recursively find a palindromic expression that evaluates to n.
    Returns the expression string if found, else None.
    """
    if depth > max_depth:
        return None
    
    if n in memo:
        return memo[n]
    
    result = None
    
    # Base case: n itself is a valid palindrome number
    n_str = str(n)
    if is_palindrome(n_str) and is_valid_number_string(n_str):
        result = n_str
    else:
        # Recursive case: try a*inner*a pattern
        # Get divisors to try as 'a'
        divisors = get_divisors(n)
        
        for a in divisors:
            if a == 1 or a == n:
                continue
            
            # Check if n is divisible by a*a
            if n % (a * a) == 0:
                inner_val = n // (a * a)
                
                # Recursively find palindrome for inner_val
                inner_expr = find_palindrome_expr(inner_val, max_depth, depth + 1)
                
                if inner_expr:
                    a_str = str(a)
                    if is_valid_number_string(a_str):
                        combined = f"{a_str}*{inner_expr}*{a_str}"
                        if is_valid_solution(combined):
                            result = combined
                            break
                
                # Also try a*inner_val*a as single number expression
                combined_val = f"{a}*{inner_val}*{a}"
                if is_valid_solution(combined_val):
                    result = combined_val
                    break
    
    memo[n] = result
    return result

def solve(n):
    # Quick check: if n itself is a palindrome number
    n_str = str(n)
    if is_palindrome(n_str) and is_valid_number_string(n_str):
        return n_str
    
    # Try single digit multiplications d*k*d
    for d in range(1, 10):
        if n % d == 0:
            k = n // d
            k_str = str(k)
            if is_valid_number_string(k_str):
                result = f"{d}*{k_str}*{d}"
                if is_valid_solution(result) and evaluate_expr(result) == n:
                    return result
    
    # Try patterns a*b*a where a and b are numbers
    divisors = get_divisors(n)
    
    for a in divisors:
        if a == 1 or a == n:
            continue
        if n % (a * a) == 0:
            b = n // (a * a)
            a_str = str(a)
            b_str = str(b)
            
            if is_valid_number_string(a_str) and is_valid_number_string(b_str):
                result = f"{a_str}*{b_str}*{a_str}"
                if is_valid_solution(result):
                    return result
    
    # Try patterns a*b*c*b*a where a, b, c are all numbers
    for a in divisors:
        if a == 1 or a == n:
            continue
        if n % (a * a) != 0:
            continue
        
        remainder = n // (a * a)
        for b in get_divisors(remainder):
            if b == 1 or b == remainder:
                continue
            if remainder % (b * b) != 0:
                continue
            
            c = remainder // (b * b)
            a_str = str(a)
            b_str = str(b)
            c_str = str(c)
            
            if (is_valid_number_string(a_str) and 
                is_valid_number_string(b_str) and 
                is_valid_number_string(c_str)):
                result = f"{a_str}*{b_str}*{c_str}*{b_str}*{a_str}"
                if is_valid_solution(result):
                    return result
    
    # Try patterns a*b*c*d*c*b*a where a, b, c, d are all numbers
    for a in divisors:
        if a == 1 or a == n:
            continue
        if n % (a * a) != 0:
            continue
        
        remainder = n // (a * a)
        for b in get_divisors(remainder):
            if b == 1 or b == remainder:
                continue
            if remainder % (b * b) != 0:
                continue
            
            remainder2 = remainder // (b * b)
            for c in get_divisors(remainder2):
                if c == 1 or c == remainder2:
                    continue
                if remainder2 % (c * c) != 0:
                    continue
                
                d = remainder2 // (c * c)
                a_str = str(a)
                b_str = str(b)
                c_str = str(c)
                d_str = str(d)
                
                if (is_valid_number_string(a_str) and 
                    is_valid_number_string(b_str) and 
                    is_valid_number_string(c_str) and
                    is_valid_number_string(d_str)):
                    result = f"{a_str}*{b_str}*{c_str}*{d_str}*{c_str}*{b_str}*{a_str}"
                    if len(result) <= 1000 and is_valid_solution(result):
                        return result
    
    return "-1"

n = int(input())
print(solve(n))
