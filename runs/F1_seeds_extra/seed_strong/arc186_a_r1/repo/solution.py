import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); Q = int(data[1])
    Ks = [int(x) for x in data[2:2 + Q]]
    # dp[R][C]: bitset of achievable totals of sum r*c using exactly R rows and C cols
    # (blocks with r,c >= 2 are free submatrices; others are fixed cells)
    dp = [[0] * (N + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    for R in range(N + 1):
        for C in range(N + 1):
            if R == 0 and C == 0:
                continue
            acc = 0
            for r in range(2, R + 1):
                for c in range(2, C + 1):
                    b = dp[R - r][C - c]
                    if b:
                        acc |= b << (r * c)
            dp[R][C] = acc
    # Allow unused rows/columns: take OR over R<=N, C<=N
    reach = 0
    for R in range(N + 1):
        for C in range(N + 1):
            reach |= dp[R][C]
    # reach bit v means v non-fixed cells achievable
    out = []
    for K in Ks:
        nf = N * N - K
        ok = 0 <= nf <= N * N and (reach >> nf) & 1
        out.append("Yes" if ok else "No")
    print("\n".join(out))

main()
