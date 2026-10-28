# Write your solution here. Read from stdin, write to stdout.

def mex(a, b, c):
    """Calculate the minimum excludant (mex) of three values"""
    values = {a, b, c}
    for i in range(4):
        if i not in values:
            return i
    return 4

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Find all tuples (i, j, k) where i < j < k and S[i:i+3] == "MEX"
    # We need to iterate through all positions where we could have "MEX"
    for i in range(n):
        if S[i] == 'M':
            for j in range(i + 1, n):
                if S[j] == 'E':
                    for k in range(j + 1, n):
                        if S[k] == 'X':
                            # Found a valid tuple (i, j, k)
                            mex_value = mex(A[i], A[j], A[k])
                            total += mex_value
    
    print(total)

solve()
