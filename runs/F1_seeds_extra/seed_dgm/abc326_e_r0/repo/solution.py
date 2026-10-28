import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [0] + [int(v) % MOD for v in data[1:1 + n]]
    invN = pow(n, MOD - 2, MOD)
    T = 0  # sum over y > x of (A_y + E_y)
    E = 0
    for x in range(n, -1, -1):
        E = T * invN % MOD
        if x >= 1:
            T = (T + A[x] + E) % MOD
    print(E % MOD)

main()
