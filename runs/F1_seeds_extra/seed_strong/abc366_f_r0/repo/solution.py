import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    funcs = []
    idx = 2
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        funcs.append((a, b))
    # Exchange argument: applying i before j (adjacent) is better iff
    # B_i/(A_i-1) > B_j/(A_j-1), with A=1 treated as infinite ratio.
    def key(f):
        a, b = f
        if a == 1:
            return (0, 0.0)
        return (1, -b / (a - 1))
    funcs.sort(key=key)
    # dp[j] = max value after applying j chosen functions (in sorted order)
    NEG = -1
    dp = [NEG] * (k + 1)
    dp[0] = 1
    for a, b in funcs:
        for j in range(k, 0, -1):
            prev = dp[j - 1]
            if prev >= 0:
                v = a * prev + b
                if v > dp[j]:
                    dp[j] = v
    print(dp[k])


main()
