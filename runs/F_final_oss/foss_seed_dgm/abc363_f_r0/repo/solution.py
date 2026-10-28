# Write your solution here. Read from stdin, write to stdout.

import sys

def no_zero(num: int) -> bool:
    return '0' not in str(num)

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    # If N itself has no zero digit, we can use the simple palindrome 1*N*1
    if no_zero(N):
        # This always forms a palindrome and evaluates to N.
        print(f"1*{N}*1")
        return
    limit = int(N ** 0.5) + 1
    for a in range(1, limit + 1):
        if N % (a * a) != 0:
            continue
        if not no_zero(a):
            continue
        b = N // (a * a)
        if no_zero(b):
            print(f"{a}*{b}*{a}")
            return
    # If not found, output -1
    print(-1)

if __name__ == "__main__":
    solve()
