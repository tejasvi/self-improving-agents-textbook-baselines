# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    input = sys.stdin.readline
    H_W_N = input().split()
    while len(H_W_N) < 3:
        # In case of empty lines (shouldn't happen)
        line = input()
        if not line:
            break
        H_W_N += line.split()
    if not H_W_N:
        return
    H, W, N = map(int, H_W_N)
    # Initialize grid with zeros (0 means no hole, 1 means hole)
    grid = [bytearray(W) for _ in range(H)]
    for _ in range(N):
        a_str = input().split()
        while len(a_str) < 2:
            a_str += input().split()
        a, b = map(int, a_str)
        grid[a - 1][b - 1] = 1
    # DP: dp[j] = size of largest hole‑less square whose bottom‑right corner is at (i, j)
    # We keep only the previous row.
    prev = [0] * (W + 1)
    ans = 0
    for i in range(1, H + 1):
        row = grid[i - 1]
        cur = [0] * (W + 1)
        for j in range(1, W + 1):
            if row[j - 1] == 0:  # not a hole
                # size = 1 + min(prev[j], cur[j-1], prev[j-1])
                a = prev[j]
                b = cur[j - 1]
                c = prev[j - 1]
                m = a if a < b else b
                if c < m:
                    m = c
                size = 1 + m
                cur[j] = size
                ans += size
            # else cur[j] stays 0
        prev = cur
    print(ans)

if __name__ == "__main__":
    solve()
