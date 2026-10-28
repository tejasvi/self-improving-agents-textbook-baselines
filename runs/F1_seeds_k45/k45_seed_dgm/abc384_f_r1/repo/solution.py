def f(x):
    """Remove all factors of 2 from x (divide by 2 while x is even)"""
    while x % 2 == 0:
        x //= 2
    return x

def main():
    n = int(input())
    a = list(map(int, input().split()))
    
    result = 0
    for i in range(n):
        for j in range(i, n):
            result += f(a[i] + a[j])
    
    print(result)

if __name__ == "__main__":
    main()
