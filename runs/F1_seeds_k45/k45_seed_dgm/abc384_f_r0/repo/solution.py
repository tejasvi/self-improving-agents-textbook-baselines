def f(x):
    """Remove all factors of 2 from x"""
    while x % 2 == 0:
        x //= 2
    return x

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = 0
    for i in range(n):
        for j in range(i, n):
            total += f(a[i] + a[j])
    
    print(total)

solve()
