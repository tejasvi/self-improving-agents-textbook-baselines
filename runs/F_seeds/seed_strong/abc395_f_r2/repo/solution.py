import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [0] * n
    D = [0] * n
    total = 0
    for i in range(n):
        u = int(data[2 + 2 * i])
        d = int(data[3 + 2 * i])
        U[i] = u
        D[i] = d
        total += u + d
    # base[i] = min_j (U[j] + x*|i-j|)
    base = U[:]
    for i in range(1, n):
        v = base[i - 1] + x
        if v < base[i]:
            base[i] = v
    for i in range(n - 2, -1, -1):
        v = base[i + 1] + x
        if v < base[i]:
            base[i] = v
    H = min(base[k] + D[k] for k in range(n))
    print(total - n * H)


main()
