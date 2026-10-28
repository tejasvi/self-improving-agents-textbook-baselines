# Teleporting Takahashi 2 solution
import sys
MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    for _ in range(M):
        X = int(next(it)) - 1  # to 0‑based
        Y = int(next(it)) - 1
        edges.append((X, Y))

    # dp[i] holds the number of ways to be at vertex (i + off) % N.
    dp = [0] * N
    dp[0] = 1  # start at vertex 1 (index 0)
    off = 0   # current offset

    for _ in range(K):
        new_off = (off + 1) % N  # default edge moves everyone forward by one
        # First collect all contributions from extra edges using the state before this step.
        adds = []
        for X, Y in edges:
            idxX = X - off
            if idxX < 0:
                idxX += N
            val = dp[idxX]
            if val:
                idxY = Y - new_off
                if idxY < 0:
                    idxY += N
                adds.append((idxY, val))
        # Apply the collected contributions.
        for idxY, val in adds:
            dp[idxY] = (dp[idxY] + val) % MOD
        off = new_off

    # Vertex 1 corresponds to index (-off) % N after the final shift.
    ans_idx = (-off) % N
    print(dp[ans_idx] % MOD)

if __name__ == "__main__":
    solve()
