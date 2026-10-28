import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [0] + [int(v) for v in data[1:1 + n]]
    invn = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]), E[N] = 0
    # S = sum_{y>x} (A_y + E[y]); going x = N-1 .. 0
    S = 0
    E = 0
    for x in range(n, -1, -1):
        if x == n:
            E = 0
        else:
            E = S * invn % MOD
        # now S should include y > x-1, i.e. add term for y = x
        if x >= 1:
            S = (S + A[x] + E) % MOD
        else:
            return print(E % MOD)

main()
