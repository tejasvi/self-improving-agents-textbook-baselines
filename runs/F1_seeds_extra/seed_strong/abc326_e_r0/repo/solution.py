import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]  # A[i] is A_{i+1}
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = inv_n * sum_{y>x} (A_y + E[y]); E[N] = 0
    E = [0] * (n + 1)
    T = 0
    for x in range(n - 1, -1, -1):
        # add y = x+1
        T = (T + A[x] + E[x + 1]) % MOD
        E[x] = T * inv_n % MOD
    print(E[0] % MOD)

main()
