import sys


def main():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(v) for v in data[1:1 + n]]
    inv_n = pow(n, MOD - 2, MOD)
    # E[x] = (1/N) * sum_{y>x} (A_y + E[y]), E[N] = 0.
    # Process x from N down to 0, maintaining T = sum_{y>x} (A_y + E[y]).
    T = 0
    e = 0  # E[N]
    for x in range(n, 0, -1):
        # add term for y = x: A_x + E[x]
        T = (T + a[x - 1] + e) % MOD
        # E[x-1] = T / N
        e = T * inv_n % MOD
    print(e)


if __name__ == "__main__":
    main()
