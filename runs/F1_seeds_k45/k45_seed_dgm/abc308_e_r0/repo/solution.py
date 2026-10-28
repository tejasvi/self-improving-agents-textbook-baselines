def mex(a, b, c):
    """Calculate mex of three values from {0, 1, 2}"""
    s = {a, b, c}
    for i in range(4):
        if i not in s:
            return i
    return 0

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Find all positions of M, E, X in string S
    m_positions = []
    e_positions = []
    x_positions = []
    
    for i in range(n):
        if S[i] == 'M':
            m_positions.append(i)
        elif S[i] == 'E':
            e_positions.append(i)
        elif S[i] == 'X':
            x_positions.append(i)
    
    # For each M position, find E positions after it, and X positions after E
    for m_idx in m_positions:
        for e_idx in e_positions:
            if e_idx > m_idx:
                for x_idx in x_positions:
                    if x_idx > e_idx:
                        total += mex(A[m_idx], A[e_idx], A[x_idx])
    
    print(total)

solve()
