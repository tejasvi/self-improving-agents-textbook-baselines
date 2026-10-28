# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    extra = []
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        extra.append((x, y))
    dp = [0] * N
    dp[0] = 1  # vertex 1 (0-index)
    offset = 0  # current offset: dp[i] corresponds to vertex (i + offset) % N
    for _ in range(K):
        offset = (offset + 1) % N  # default edge moves everyone forward
        # add contributions of extra edges
        for x, y in extra:
            # index of vertex x before the move (offset_old = offset-1)
            i = (x - 1 - (offset - 1)) % N
            # index of vertex y after the move (offset is already updated)
            j = (y - 1 - offset) % N
            dp[j] = (dp[j] + dp[i]) % MOD
    ans = sum(dp) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
