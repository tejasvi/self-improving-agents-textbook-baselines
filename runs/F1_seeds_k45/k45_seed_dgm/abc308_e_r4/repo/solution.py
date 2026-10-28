def calculate_mex(a, b, c):
    """Calculate the minimum excludant (mex) of three values."""
    # mex is the smallest non-negative integer not in the set
    values = {a, b, c}
    mex = 0
    while mex in values:
        mex += 1
    return mex


def solve():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Find all tuples (i, j, k) where i < j < k and S[i] = 'M', S[j] = 'E', S[k] = 'X'
    for i in range(n):
        if S[i] != 'M':
            continue
        for j in range(i + 1, n):
            if S[j] != 'E':
                continue
            for k in range(j + 1, n):
                if S[k] != 'X':
                    continue
                # Found a valid tuple
                mex_value = calculate_mex(A[i], A[j], A[k])
                total += mex_value
    
    print(total)


if __name__ == "__main__":
    solve()
