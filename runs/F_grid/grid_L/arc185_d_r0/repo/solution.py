import sys

MOD = 998244353


def main():
    N, M = map(int, sys.stdin.read().split())
    # Cover time = M^2 * ( sum_{s=0}^{N-1} (N+s)/(N-s) + (N-1) )
    # Derived from: each chain is a path of length M hanging off the root;
    # the walk must reach all N leaves.
    # inv[k] for k = 1..N via linear recurrence
    inv = [0, 1] + [0] * (N)
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
    total = 0
    for s in range(N):
        total = (total + (N + s) * inv[N - s]) % MOD
    total = (total + N - 1) % MOD
    ans = total * (M * M % MOD) % MOD
    print(ans)


main()
