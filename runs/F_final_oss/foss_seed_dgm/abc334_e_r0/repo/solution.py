import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    grid = [list(next(it).strip()) for _ in range(H)]

    # component ids for green cells ('#')
    comp = [[-1] * W for _ in range(H)]
    from collections import deque
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    comp_cnt = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#' and comp[i][j] == -1:
                # BFS
                dq = deque()
                dq.append((i,j))
                comp[i][j] = comp_cnt
                while dq:
                    x,y = dq.popleft()
                    for dx,dy in dirs:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == '#' and comp[nx][ny] == -1:
                            comp[nx][ny] = comp_cnt
                            dq.append((nx,ny))
                comp_cnt += 1
    C = comp_cnt  # initial number of green components

    total_red = 0
    sum1 = 0  # sum of (1 - k) over red cells
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                total_red += 1
                neighbor_ids = set()
                for dx,dy in dirs:
                    nx, ny = i+dx, j+dy
                    if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == '#':
                        neighbor_ids.add(comp[nx][ny])
                k = len(neighbor_ids)
                sum1 += 1 - k
    # compute answer modulo MOD
    invR = pow(total_red, MOD-2, MOD)
    ans = (C % MOD + (sum1 % MOD) * invR) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
