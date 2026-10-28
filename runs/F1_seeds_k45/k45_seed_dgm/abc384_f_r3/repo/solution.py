def f(x):
    """
    For a positive integer x, keep dividing by 2 while x is even.
    Return the final value (the odd part of x).
    """
    while x % 2 == 0:
        x //= 2
    return x

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = 0
    # Iterate through all pairs (i, j) where i <= j
    for i in range(n):
        for j in range(i, n):
            total += f(a[i] + a[j])
    
    print(total)

if __name__ == "__main__":
    main()
