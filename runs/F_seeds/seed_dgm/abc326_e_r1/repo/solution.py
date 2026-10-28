import sys

def main():
    data = sys.stdin.buffer.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    invN = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]),  E[N] = 0
    # Process x from N down to 0, maintaining T = sum_{y>x} (A_y + E[y]).
    T = 0
    E = 0  # E[N]
    for x in range(n, 0, -1):
        # E for x (computed as T/N, where T covers y > x)
        if x == n:
            E = 0
        else:
            E = T * invN % MOD
        T = (T + A[x - 1] + E) % MOD
    E0 = T * invN % MOD
    print(E0)

main()
