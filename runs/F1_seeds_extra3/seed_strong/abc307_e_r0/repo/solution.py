import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    MOD = 998244353
    # Proper colorings of cycle C_n with m colors: (m-1)^n + (-1)^n (m-1)
    ans = (pow(m - 1, n, MOD) + (m - 1 if n % 2 == 0 else -(m - 1))) % MOD
    print(ans)

main()
