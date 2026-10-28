#!/usr/bin/env python3
import sys
sys.setrecursionlimit(1 << 25)

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    grid = [list(next(it).strip()) for _ in range(H)]

    # Component id for green cells ('#'), -1 for red ('.')
    comp = [[-1]*W for _ in range(H)]
    from collections import deque
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
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == '#' and comp[nx][ny] == -1:
                            comp[nx][ny] = comp_cnt
                            dq.append((nx,ny))
                comp_cnt += 1
    # Count red cells and sum of distinct neighboring components
    red_cnt = 0
    sum_k = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                red_cnt += 1
                neigh = set()
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = i+dx, j+dy
                    if 0 <= nx < H and 0 <= ny < W:
                        cid = comp[nx][ny]
                        if cid != -1:
                            neigh.add(cid)
                sum_k += len(neigh)
    # Expected value = C0 + (R - sum_k)/R
    C0 = comp_cnt
    R = red_cnt
    # Compute numerator P = C0*R + (R - sum_k)
    P = (C0 * R + (R - sum_k)) % MOD
    invR = pow(R, MOD-2, MOD)
    ans = P * invR % MOD
    print(ans)

if __name__ == "__main__":
    main()
