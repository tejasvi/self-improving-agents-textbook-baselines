# Write your solution here. Read from stdin, write to stdout.

def f(x):
    """
    Remove all factors of 2 from x.
    While x is even, divide by 2.
    Return the final odd value.
    """
    while x % 2 == 0:
        x //= 2
    return x

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    result = 0
    for i in range(n):
        for j in range(i, n):
            result += f(a[i] + a[j])
    
    print(result)

solve()
