def f(x):
    """Remove all factors of 2 from x, returning the odd part."""
    while x % 2 == 0:
        x //= 2
    return x


def main():
    N = int(input())
    A = list(map(int, input().split()))
    
    result = 0
    for i in range(N):
        for j in range(i, N):
            result += f(A[i] + A[j])
    
    print(result)


if __name__ == "__main__":
    main()
