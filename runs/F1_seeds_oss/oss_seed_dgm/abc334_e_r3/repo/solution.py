# Write your solution here. Read from stdin, write to stdout.
import sys
from collections import deque

def solve():
    MOD = 998244353
    data = sys.stdin.read().splitlines()
    if not data:
        return
    H, W = map(int, data[0].split())
    grid = [list(line.strip()) for line in data[1:1+H]]
    # component ids for green cells ('#')
    comp_id = [[-1] * W for _ in range(H)]
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]
    comp_cnt = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and comp_id[i][j] == -1:
                # BFS to label component
                dq = deque()
                dq.append((i,j))
                comp_id[i][j] = comp_cnt
                while dq:
                    x, y = dq.popleft()
                    for dx, dy in dirs:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < H and 0 <= ny < W:
                            if grid[nx][ny] == '#' and comp_id[nx][ny] == -1:
                                comp_id[nx][ny] = comp_cnt
                                dq.append((nx, ny))
                comp_cnt += 1
    # count red cells and sum of distinct neighboring components for each red cell
    red_cnt = 0
    total_k = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cnt += 1
                seen = []
                for dx, dy in dirs:
                    ni, nj = i+dx, j+dy
                    if 0 <= ni < H and 0 <= nj < W and grid[ni][nj] == '#':
                        cid = comp_id[ni][nj]
                        # deduplicate manually (at most 4 items)
                        if cid not in seen:
                            seen.append(cid)
                total_k += len(seen)
    # expected value = C0 + 1 - total_k / red_cnt
    inv_red = pow(red_cnt, MOD-2, MOD)
    ans = ( (comp_cnt + 1) % MOD - (total_k % MOD) * inv_red % MOD ) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
