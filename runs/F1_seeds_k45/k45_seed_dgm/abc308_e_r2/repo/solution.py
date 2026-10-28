def mex(a, b, c):
    """Calculate minimum excludant of three values"""
    s = {a, b, c}
    for i in range(4):
        if i not in s:
            return i
    return 4

def main():
    n = int(input())
    A = list(map(int, input().split()))
    S = input().strip()
    
    total = 0
    
    # Brute force approach: check all tuples (i,j,k)
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
                mex_val = mex(A[i], A[j], A[k])
                total += mex_val
    
    print(total)

if __name__ == "__main__":
    main()
