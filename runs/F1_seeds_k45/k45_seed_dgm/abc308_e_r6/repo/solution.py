# Write your solution here. Read from stdin, write to stdout.

def mex(a, b, c):
    """Calculate the minimum excludant (MEX) of three values."""
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
    
    # Find all tuples (i, j, k) where S[i]S[j]S[k] = "MEX"
    # We need i < j < k (0-indexed: i < j < k)
    for j in range(1, n - 1):  # j can be from 1 to n-2 (0-indexed)
        if S[j] == 'E':
            # Find all i < j where S[i] = 'M'
            for i in range(j):
                if S[i] == 'M':
                    # Find all k > j where S[k] = 'X'
                    for k in range(j + 1, n):
                        if S[k] == 'X':
                            total += mex(A[i], A[j], A[k])
    
    print(total)

if __name__ == "__main__":
    main()
