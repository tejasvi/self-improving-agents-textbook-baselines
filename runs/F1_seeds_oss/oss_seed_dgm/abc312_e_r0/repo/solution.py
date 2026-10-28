# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    cuboids = []
    max_coord = 100  # given upper bound
    for _ in range(N):
        x1 = int(next(it)); y1 = int(next(it)); z1 = int(next(it))
        x2 = int(next(it)); y2 = int(next(it)); z2 = int(next(it))
        cuboids.append((x1, y1, z1, x2, y2, z2))
    # 3D grid of size 100x100x100 representing unit cells [x,x+1) etc.
    MAX = max_coord
    size = MAX * MAX * MAX
    grid = [0] * size  # store cuboid id (1-indexed) occupying each unit cell
    # Fill grid
    for idx, (x1, y1, z1, x2, y2, z2) in enumerate(cuboids, start=1):
        for x in range(x1, x2):
            base_x = x * MAX * MAX
            for y in range(y1, y2):
                base_xy = base_x + y * MAX
                for z in range(z1, z2):
                    grid[base_xy + z] = idx
    # Find adjacent pairs across faces
    pairs = set()
    for x in range(MAX):
        base_x = x * MAX * MAX
        for y in range(MAX):
            base_xy = base_x + y * MAX
            for z in range(MAX):
                a = grid[base_xy + z]
                if a == 0:
                    continue
                # +x direction
                if x + 1 < MAX:
                    b = grid[base_xy + z + MAX * MAX]
                    if b and b != a:
                        if a < b:
                            pairs.add((a, b))
                        else:
                            pairs.add((b, a))
                # +y direction
                if y + 1 < MAX:
                    b = grid[base_xy + z + MAX]
                    if b and b != a:
                        if a < b:
                            pairs.add((a, b))
                        else:
                            pairs.add((b, a))
                # +z direction
                if z + 1 < MAX:
                    b = grid[base_xy + z + 1]
                    if b and b != a:
                        if a < b:
                            pairs.add((a, b))
                        else:
                            pairs.add((b, a))
    ans = [0] * (N + 1)
    for i, j in pairs:
        ans[i] += 1
        ans[j] += 1
    out = "\n".join(str(ans[i]) for i in range(1, N + 1))
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()
