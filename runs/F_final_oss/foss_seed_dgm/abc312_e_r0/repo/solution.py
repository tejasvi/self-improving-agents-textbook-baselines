#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    cuboids = []
    for _ in range(N):
        x1 = int(next(it)); y1 = int(next(it)); z1 = int(next(it))
        x2 = int(next(it)); y2 = int(next(it)); z2 = int(next(it))
        cuboids.append((x1, y1, z1, x2, y2, z2))

    MAX = 100  # maximum coordinate value
    # 3D grid: store cuboid index occupying each unit cell, -1 if empty
    # size MAX x MAX x MAX (indices 0..MAX-1)
    grid = [[[-1] * MAX for _ in range(MAX)] for _ in range(MAX)]
    # Fill the grid; total occupied cells (volume) <= 1e6
    for idx, (x1, y1, z1, x2, y2, z2) in enumerate(cuboids):
        for x in range(x1, x2):
            gx = grid[x]
            for y in range(y1, y2):
                gy = gx[y]
                for z in range(z1, z2):
                    gy[z] = idx

    cnt = [0] * N
    seen_pairs = set()
    # Directions: +x, +y, +z to avoid double counting
    for x in range(MAX):
        for y in range(MAX):
            for z in range(MAX):
                id1 = grid[x][y][z]
                if id1 == -1:
                    continue
                # +x neighbor
                if x + 1 < MAX:
                    id2 = grid[x + 1][y][z]
                    if id2 != -1 and id2 != id1:
                        a, b = (id1, id2) if id1 < id2 else (id2, id1)
                        if (a, b) not in seen_pairs:
                            seen_pairs.add((a, b))
                            cnt[a] += 1
                            cnt[b] += 1
                # +y neighbor
                if y + 1 < MAX:
                    id2 = grid[x][y + 1][z]
                    if id2 != -1 and id2 != id1:
                        a, b = (id1, id2) if id1 < id2 else (id2, id1)
                        if (a, b) not in seen_pairs:
                            seen_pairs.add((a, b))
                            cnt[a] += 1
                            cnt[b] += 1
                # +z neighbor
                if z + 1 < MAX:
                    id2 = grid[x][y][z + 1]
                    if id2 != -1 and id2 != id1:
                        a, b = (id1, id2) if id1 < id2 else (id2, id1)
                        if (a, b) not in seen_pairs:
                            seen_pairs.add((a, b))
                            cnt[a] += 1
                            cnt[b] += 1
    sys.stdout.write("\n".join(map(str, cnt)))

if __name__ == "__main__":
    solve()
