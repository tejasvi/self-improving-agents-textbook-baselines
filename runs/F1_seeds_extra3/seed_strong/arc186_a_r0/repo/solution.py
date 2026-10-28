import sys

def achievable_nonfixed(N):
    # reach[r][c]: bitmask of total block-area S achievable using exactly r rows and c cols
    reach = [[0] * (N + 1) for _ in range(N + 1)]
    reach[0][0] = 1
    for r in range(N + 1):
        for c in range(N + 1):
            cur = reach[r][c]
            if not cur:
                continue
            for a in range(2, N - r + 1):
                for b in range(2, N - c + 1):
                    reach[r + a][c + b] |= cur << (a * b)
    total = 0
    for r in range(N + 1):
        for c in range(N + 1):
            total |= reach[r][c]
    return total

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); Q = int(data[1])
    ach = achievable_nonfixed(N)
    out = []
    for i in range(Q):
        K = int(data[2 + i])
        S = N * N - K
        out.append("Yes" if 0 <= S <= N * N and (ach >> S) & 1 else "No")
    print("\n".join(out))

main()
