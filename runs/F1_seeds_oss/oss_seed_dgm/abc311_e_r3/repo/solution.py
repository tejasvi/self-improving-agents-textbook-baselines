# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = int(next(it))
    # use bytearray per row to store holes (1 = hole)
    hole = [bytearray(W) for _ in range(H)]
    for _ in range(N):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        hole[a][b] = 1
    dp_prev = [0] * W
    total = 0
    for i in range(H):
        dp_curr = [0] * W
        row = hole[i]
        for j in range(W):
            if row[j]:
                dp_curr[j] = 0
            else:
                if i == 0 or j == 0:
                    dp_curr[j] = 1
                else:
                    # classic DP for largest square ending at (i,j)
                    dp_curr[j] = 1 + min(dp_prev[j], dp_curr[j-1], dp_prev[j-1])
            total += dp_curr[j]
        dp_prev = dp_curr
    print(total)

if __name__ == "__main__":
    solve()
