import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    x = [int(v) for v in data[1:1 + n]]
    # gaps g_k = x[k] - x[k-1] for k = 1..n-1 (1-indexed)
    # operation swaps gaps g_i and g_{i+2}; so each parity class can be permuted freely.
    # sum = n*x[0] + sum_k (n-k) * g_k ; minimize within each parity class.
    total = n * x[0]
    for parity in (1, 0):
        gaps = []
        weights = []
        for k in range(1, n):
            if k % 2 == parity:
                gaps.append(x[k] - x[k - 1])
                weights.append(n - k)
        gaps.sort()
        weights.sort(reverse=True)
        total += sum(g * w for g, w in zip(gaps, weights))
    print(total)


main()
