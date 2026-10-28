def mex(a, b, c):
    """Calculate the MEX (minimum excludant) of three values."""
    values = {a, b, c}
    # MEX is the smallest non-negative integer not in the set
    for i in range(4):
        if i not in values:
            return i
    return 0


def solve():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Iterate through all tuples (i, j, k) with i < j < k
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
                total += mex(A[i], A[j], A[k])
    
    print(total)


if __name__ == "__main__":
    solve()
