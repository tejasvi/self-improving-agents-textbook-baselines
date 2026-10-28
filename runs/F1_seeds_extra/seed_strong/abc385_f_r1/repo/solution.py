import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    xs = [int(v) for v in data[1::2][:n]]
    hs = [int(v) for v in data[2::2][:n]]
    if n == 1:
        print(-1)
        return
    # Threshold for adjacent pair (k, k+1): (H_k*X_{k+1} - H_{k+1}*X_k) / (X_{k+1} - X_k)
    best_num = None
    best_den = 1
    for k in range(n - 1):
        num = hs[k] * xs[k + 1] - hs[k + 1] * xs[k]
        den = xs[k + 1] - xs[k]
        if best_num is None or num * best_den > best_num * den:
            best_num, best_den = num, den
    if best_num < 0:
        print(-1)
        return
    ans = best_num / best_den
    print("%.18f" % ans)


main()
