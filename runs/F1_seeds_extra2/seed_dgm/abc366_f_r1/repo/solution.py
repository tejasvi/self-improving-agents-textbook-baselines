import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    funcs = []
    idx = 2
    for _ in range(n):
        a = int(data[idx]); b = int(data[idx + 1])
        idx += 2
        funcs.append((a, b))
    # Optimal chain: inner functions have smaller (A-1)/B ratio.
    funcs.sort(key=lambda t: (t[0] - 1) / t[1])
    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            if dp[j - 1] is not None:
                v = a * dp[j - 1] + b
                if dp[j] is None or v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
