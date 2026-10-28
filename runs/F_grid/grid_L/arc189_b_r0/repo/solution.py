import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    x = [int(v) for v in data[1:1 + n]]
    # gaps d[k] = x[k+1] - x[k], k = 0..n-2 (0-indexed)
    gaps = [x[k + 1] - x[k] for k in range(n - 1)]
    # Operation reverses a window of 3 consecutive gaps: swaps gaps at
    # indices j and j+2 (same parity), so each parity class can be permuted freely.
    new_gaps = [0] * (n - 1)
    for par in (0, 1):
        idx = list(range(par, n - 1, 2))
        vals = sorted(gaps[k] for k in idx)
        for k, v in zip(idx, vals):
            new_gaps[k] = v
    # Sum of coordinates: x_0 * n + sum_k (n-1-k) * gap_k (0-indexed gap k)
    total = x[0] * n
    for k in range(n - 1):
        total += (n - 1 - k) * new_gaps[k]
    print(total)


main()
