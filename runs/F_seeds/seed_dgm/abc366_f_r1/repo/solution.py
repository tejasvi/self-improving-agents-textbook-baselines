import sys



def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    funcs = []
    for i in range(n):
        a = int(data[2 + 2 * i])
        b = int(data[3 + 2 * i])
        funcs.append((a, b))
    # Applied-first (innermost) functions should have smaller (A-1)/B.
    funcs.sort(key=lambda t: (t[0] - 1) / t[1])
    NEG = None
    dp = [NEG] * (k + 1)
    dp[0] = 1  # value of x=1 before applying any function
    for a, b in funcs:
        for j in range(k - 1, -1, -1):
            if dp[j] is not None:
                v = a * dp[j] + b
                if dp[j + 1] is None or v > dp[j + 1]:
                    dp[j + 1] = v
    print(dp[k])


main()
