# Write your solution here. Read from stdin, write to stdout.

def f(x):
    """
    Returns the odd part of x by dividing by 2 while x is even.
    """
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
