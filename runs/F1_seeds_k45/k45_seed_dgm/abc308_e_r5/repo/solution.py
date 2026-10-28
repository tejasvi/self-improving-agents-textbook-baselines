# Write your solution here. Read from stdin, write to stdout.

def mex(a, b, c):
    """
    Compute the minimum excluded (mex) value for three integers.
    mex returns the smallest non-negative integer not in {a, b, c}
    """
    s = {a, b, c}
    for val in range(4):
        if val not in s:
            return val
    return 3  # This would be if all 0, 1, 2 are present

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Find all tuples (i, j, k) where i < j < k and S[i]S[j]S[k] == "MEX"
    for i in range(n):
        if S[i] != 'M':
            continue
        for j in range(i + 1, n):
            if S[j] != 'E':
                continue
            for k in range(j + 1, n):
                if S[k] != 'X':
                    continue
                # Found a valid tuple (i, j, k)
                total += mex(A[i], A[j], A[k])
    
    print(total)

solve()
