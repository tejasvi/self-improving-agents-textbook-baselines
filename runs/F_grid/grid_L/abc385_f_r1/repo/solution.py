import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(data[1 + 2 * i]) for i in range(n)]
    hs = [int(data[2 + 2 * i]) for i in range(n)]
    if n == 1:
        print(-1)
        return
    # Threshold for adjacent pair (j, i), X_j < X_i:
    #   t = (H_j*X_i - H_i*X_j) / (X_i - X_j)
    best_num = None
    best_den = 1
    for k in range(n - 1):
        xj, hj = xs[k], hs[k]
        xi, hi = xs[k + 1], hs[k + 1]
        num = hj * xi - hi * xj
        den = xi - xj
        if best_num is None or num * best_den > best_num * den:
            best_num, best_den = num, den
    if best_num < 0:
        print(-1)
        return
    print("%.18f" % (best_num / best_den))


main()
