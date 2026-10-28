def f(x):
    """
    While x is even, keep dividing by 2.
    Return the final value (which will be odd).
    """
    while x % 2 == 0:
        x //= 2
    return x


def main():
    # Read input
    n = int(input())
    a = list(map(int, input().split()))
    
    # Calculate the sum
    total = 0
    for i in range(n):
        for j in range(i, n):
            total += f(a[i] + a[j])
    
    print(total)


if __name__ == "__main__":
    main()
