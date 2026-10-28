# Write your solution here. Read from stdin, write to stdout.

import sys

def has_no_zero(s: str) -> bool:
    return '0' not in s

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    sN = str(N)
    # Case 1: single number palindrome without zero
    if sN == sN[::-1] and has_no_zero(sN):
        print(sN)
        return
    # Helper to check and output a palindrome of form a*b*rev(a)
    def try_construct(a: int) -> bool:
        sa = str(a)
        if not has_no_zero(sa):
            return False
        rev_a_str = sa[::-1]
        if not has_no_zero(rev_a_str):
            return False
        rev_a = int(rev_a_str)
        prod = a * rev_a
        if prod > N:
            return False
        if N % prod != 0:
            return False
        b = N // prod
        sb = str(b)
        if not has_no_zero(sb):
            return False
        # construct palindrome string a* b * rev_a
        # If b is 1 we can still output it (makes palindrome)
        print(f"{sa}*{sb}*{rev_a_str}")
        return True
    # Iterate over divisors
    import math
    limit = int(math.isqrt(N))
    for i in range(1, limit + 1):
        if N % i == 0:
            # try divisor i as a
            if try_construct(i):
                return
            # try the counterpart divisor N//i as a (if different)
            j = N // i
            if j != i:
                if try_construct(j):
                    return
    # No solution found
    print(-1)

if __name__ == "__main__":
    solve()
