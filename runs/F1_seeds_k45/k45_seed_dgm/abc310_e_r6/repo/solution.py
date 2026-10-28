# Write your solution here. Read from stdin, write to stdout.

def nand(a, b):
    """NAND operation: returns 1 if not (a and b)"""
    return 1 - (a & b)

def main():
    N = int(input())
    S = input().strip()
    
    # Convert string to list of integers
    A = [int(ch) for ch in S]
    
    total = 0
    
    # For each starting position i
    for i in range(N):
        # Compute f(i, j) for all j >= i
        current = A[i]  # f(i, i)
        total += current
        
        # For j > i, compute f(i, j) = f(i, j-1) ⊼ A[j]
        for j in range(i + 1, N):
            current = nand(current, A[j])
            total += current
    
    print(total)

if __name__ == "__main__":
    main()
