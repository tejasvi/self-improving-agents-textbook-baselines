def nand(a, b):
    """NAND operation: returns 0 only if both a and b are 1"""
    return 0 if (a == 1 and b == 1) else 1

def main():
    N = int(input())
    S = input().strip()
    A = [int(c) for c in S]
    
    total = 0
    
    # For each starting position i
    for i in range(N):
        f_val = A[i]
        total += f_val
        
        # For each ending position j >= i
        for j in range(i + 1, N):
            f_val = nand(f_val, A[j])
            total += f_val
    
    print(total)

if __name__ == "__main__":
    main()
