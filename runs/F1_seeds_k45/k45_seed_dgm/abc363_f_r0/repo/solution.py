def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def is_valid_number(s):
    """Check if string contains only digits 1-9 (no 0s)"""
    return s and all(c in '123456789' for c in s)

def get_divisors(n, limit=1000000):
    """Get all divisors of n up to limit"""
    divisors = set()
    i = 1
    while i * i <= n and i <= limit:
        if n % i == 0:
            divisors.add(i)
            if i != n // i and n // i <= 10**15:  # Avoid very large divisors
                divisors.add(n // i)
        i += 1
    return sorted(list(divisors))

def solve(n):
    # First, check if n itself is a palindrome with valid digits
    n_str = str(n)
    if is_palindrome(n_str) and is_valid_number(n_str):
        return n_str
    
    divisors = get_divisors(n)
    
    if len(divisors) == 0:
        return "-1"
    
    # Try a*b*a pattern where a²*b = n
    for a in divisors:
        if n % (a * a) == 0:
            b = n // (a * a)
            a_str = str(a)
            b_str = str(b)
            
            if is_valid_number(a_str) and is_valid_number(b_str):
                candidate = a_str + '*' + b_str + '*' + a_str
                if is_palindrome(candidate):
                    return candidate
    
    # Try a*b*c*b*a pattern where a²*b²*c = n
    for a in divisors:
        if n % (a * a) != 0:
            continue
        remaining1 = n // (a * a)
        
        for b in divisors:
            if remaining1 % (b * b) != 0:
                continue
            c = remaining1 // (b * b)
            
            a_str = str(a)
            b_str = str(b)
            c_str = str(c)
            
            if is_valid_number(a_str) and is_valid_number(b_str) and is_valid_number(c_str):
                candidate = a_str + '*' + b_str + '*' + c_str + '*' + b_str + '*' + a_str
                if is_palindrome(candidate):
                    return candidate
    
    # Try a*b*c*d*c*b*a pattern where a²*b²*c²*d = n
    for a in divisors:
        if n % (a * a) != 0:
            continue
        remaining1 = n // (a * a)
        
        for b in divisors:
            if remaining1 % (b * b) != 0:
                continue
            remaining2 = remaining1 // (b * b)
            
            for c in divisors:
                if remaining2 % (c * c) != 0:
                    continue
                d = remaining2 // (c * c)
                
                a_str = str(a)
                b_str = str(b)
                c_str = str(c)
                d_str = str(d)
                
                if is_valid_number(a_str) and is_valid_number(b_str) and \
                   is_valid_number(c_str) and is_valid_number(d_str):
                    candidate = a_str + '*' + b_str + '*' + c_str + '*' + d_str + '*' + c_str + '*' + b_str + '*' + a_str
                    if is_palindrome(candidate):
                        return candidate
    
    return "-1"

def main():
    n = int(input().strip())
    result = solve(n)
    print(result)

if __name__ == "__main__":
    main()
