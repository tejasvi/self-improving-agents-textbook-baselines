# Write your solution here. Read from stdin, write to stdout.

def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def is_valid_number(s):
    """Check if string represents a valid number (digits 1-9 only)"""
    return all(c in '123456789' for c in s)

def reverse_number(n):
    """Reverse the digits of a number"""
    return int(str(n)[::-1])

def get_divisors_up_to(n, limit=100000):
    """Find all divisors of n up to limit, sorted"""
    divisors = []
    i = 1
    while i * i <= n and i <= limit:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                other = n // i
                if other <= limit:
                    divisors.append(other)
        i += 1
    return sorted(divisors)

def solve(n):
    # Case 1: Check if N itself is valid
    s = str(n)
    if is_valid_number(s) and is_palindrome(s):
        return s
    
    # Case 2: Single digit * palindrome where the result is also a palindrome
    for a in range(1, 10):
        if n % a == 0:
            b = n // a
            b_str = str(b)
            if is_valid_number(b_str) and is_palindrome(b_str):
                candidate = str(a) + "*" + b_str
                if is_palindrome(candidate):
                    return candidate
    
    # Case 3: Try patterns like a*b*a where a^2 * b = n
    divisors = get_divisors_up_to(n, limit=100000)
    
    for a in divisors:
        if a * a > n:
            break
        if n % (a * a) == 0:
            b = n // (a * a)
            a_str = str(a)
            b_str = str(b)
            
            if is_valid_number(a_str) and is_valid_number(b_str):
                candidate = a_str + "*" + b_str + "*" + a_str
                if is_palindrome(candidate):
                    return candidate
    
    # Case 4: Try patterns like a*b*c*b_rev*a where a * b * c * b_rev * a = n
    # and the string "a*b*c*b_rev*a" is a palindrome
    # Note: b_rev is the digit-reversal of b
    
    for a in divisors:
        if a * a > n:
            break
        if n % (a * a) != 0:
            continue
        
        remaining1 = n // (a * a)
        divisors1 = get_divisors_up_to(remaining1, limit=100000)
        
        for b in divisors1:
            if b * reverse_number(b) > remaining1:
                break
            
            if remaining1 % (b * reverse_number(b)) != 0:
                continue
            
            c = remaining1 // (b * reverse_number(b))
            
            a_str = str(a)
            b_str = str(b)
            b_rev_str = str(reverse_number(b))
            c_str = str(c)
            
            if all(is_valid_number(x) for x in [a_str, b_str, b_rev_str, c_str]):
                candidate = a_str + "*" + b_str + "*" + c_str + "*" + b_rev_str + "*" + a_str
                if is_palindrome(candidate):
                    return candidate
    
    # Case 5: Try longer patterns a*b*c*d*c_rev*b_rev*a
    for a in divisors:
        if a * a > n:
            break
        if n % (a * a) != 0:
            continue
        
        remaining1 = n // (a * a)
        divisors1 = get_divisors_up_to(remaining1, limit=100000)
        
        for b in divisors1:
            if b * reverse_number(b) > remaining1:
                break
            if remaining1 % (b * reverse_number(b)) != 0:
                continue
            
            remaining2 = remaining1 // (b * reverse_number(b))
            divisors2 = get_divisors_up_to(remaining2, limit=100000)
            
            for c in divisors2:
                if c * reverse_number(c) > remaining2:
                    break
                if remaining2 % (c * reverse_number(c)) != 0:
                    continue
                
                d = remaining2 // (c * reverse_number(c))
                
                a_str = str(a)
                b_str = str(b)
                b_rev_str = str(reverse_number(b))
                c_str = str(c)
                c_rev_str = str(reverse_number(c))
                d_str = str(d)
                
                if all(is_valid_number(x) for x in [a_str, b_str, c_str, d_str, b_rev_str, c_rev_str]):
                    candidate = a_str + "*" + b_str + "*" + c_str + "*" + d_str + "*" + c_rev_str + "*" + b_rev_str + "*" + a_str
                    if is_palindrome(candidate):
                        return candidate
    
    # Case 6: Try even longer patterns a*b*c*d*e*d_rev*c_rev*b_rev*a
    for a in divisors:
        if a * a > n:
            break
        if n % (a * a) != 0:
            continue
        
        remaining1 = n // (a * a)
        divisors1 = get_divisors_up_to(remaining1, limit=100000)
        
        for b in divisors1:
            if b * reverse_number(b) > remaining1:
                break
            if remaining1 % (b * reverse_number(b)) != 0:
                continue
            
            remaining2 = remaining1 // (b * reverse_number(b))
            divisors2 = get_divisors_up_to(remaining2, limit=100000)
            
            for c in divisors2:
                if c * reverse_number(c) > remaining2:
                    break
                if remaining2 % (c * reverse_number(c)) != 0:
                    continue
                
                remaining3 = remaining2 // (c * reverse_number(c))
                divisors3 = get_divisors_up_to(remaining3, limit=100000)
                
                for d in divisors3:
                    if d * reverse_number(d) > remaining3:
                        break
                    if remaining3 % (d * reverse_number(d)) != 0:
                        continue
                    
                    e = remaining3 // (d * reverse_number(d))
                    
                    a_str = str(a)
                    b_str = str(b)
                    b_rev_str = str(reverse_number(b))
                    c_str = str(c)
                    c_rev_str = str(reverse_number(c))
                    d_str = str(d)
                    d_rev_str = str(reverse_number(d))
                    e_str = str(e)
                    
                    if all(is_valid_number(x) for x in [a_str, b_str, c_str, d_str, e_str, b_rev_str, c_rev_str, d_rev_str]):
                        candidate = a_str + "*" + b_str + "*" + c_str + "*" + d_str + "*" + e_str + "*" + d_rev_str + "*" + c_rev_str + "*" + b_rev_str + "*" + a_str
                        if is_palindrome(candidate):
                            return candidate
    
    return "-1"

# Read input
n = int(input())
print(solve(n))
