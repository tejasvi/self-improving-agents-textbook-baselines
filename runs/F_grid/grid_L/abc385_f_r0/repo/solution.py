import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1:1 + 2 * n:2]]
    hs = [int(v) for v in data[2:2 + 2 * n:2]]

    # Max y-intercept (at x=0) over lines through adjacent building tops.
    # For adjacent j, i=j+1: intercept = (H_j*X_i - H_i*X_j) / (X_i - X_j)
    best_num = None
    best_den = None
    for j in range(n - 1):
        xj, hj = xs[j], hs[j]
        xi, hi = xs[j + 1], hs[j + 1]
        num = hj * xi - hi * xj
        den = xi - xj  # > 0
        if best_num is None or num * best_den > best_num * den:
            best_num, best_den = num, den

    if best_num is None or best_num < 0:
        # Visible from (0,0) only if max intercept < 0 (or no pairs)
        print(-1)
        return

    # Print best_num / best_den with 18 decimals, exact integer arithmetic
    scale = 10 ** 18
    q = (best_num * scale * 2 + best_den) // (2 * best_den)  # rounded
    int_part, frac_part = divmod(q, scale)
    print(f"{int_part}.{frac_part:018d}")


main()
