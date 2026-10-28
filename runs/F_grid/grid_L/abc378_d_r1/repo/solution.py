import sys


def main():
    data = sys.stdin.read().split()
    H, W, K = int(data[0]), int(data[1]), int(data[2])
    rows = data[3:3 + H]
    # padded grid of size (H+2) x (W+2); border cells are blocked
    W2 = W + 2
    free = [False] * ((H + 2) * W2)
    for i in range(H):
        for j in range(W):
            if rows[i][j] == '.':
                free[(i + 1) * W2 + (j + 1)] = True
    visited = [False] * ((H + 2) * W2)
    dirs = (1, -1, W2, -W2)
    sys.setrecursionlimit(10000)

    def dfs(pos, remaining):
        # pos is currently visited; count walks of `remaining` more moves
        if remaining == 0:
            return 1
        total = 0
        visited[pos] = True
        for d in dirs:
            nxt = pos + d
            if free[nxt] and not visited[nxt]:
                total += dfs(nxt, remaining - 1)
        visited[pos] = False
        return total

    ans = 0
    for i in range(H):
        for j in range(W):
            p = (i + 1) * W2 + (j + 1)
            if free[p]:
                ans += dfs(p, K)
    print(ans)


main()
