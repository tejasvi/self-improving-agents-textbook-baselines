import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    M = 101
    MM = M * M
    grid = [-1] * (M * MM)
    rows = []
    p = 1
    for i in range(n):
        x1, y1, z1, x2, y2, z2 = (int(v) for v in data[p:p + 6])
        p += 6
        rows.append((x1, y1, z1, x2, y2, z2))
        # fill cells (x,y,z) for x in [x1,x2), y in [y1,y2), z in [z1,z2)
        zl = z2 - z1
        seg = [i] * zl
        for x in range(x1, x2):
            base = x * MM
            for y in range(y1, y2):
                s = base + y * M + z1
                grid[s:s + zl] = seg
    ans = [0] * n
    for i, (x1, y1, z1, x2, y2, z2) in enumerate(rows):
        nb = set()
        faces = []
        if x2 < M:
            faces.append([(x2 * MM + y * M + z) for y in range(y1, y2) for z in range(z1, z2)])
        if x1 >= 1:
            faces.append([((x1 - 1) * MM + y * M + z) for y in range(y1, y2) for z in range(z1, z2)])
        if y2 < M:
            faces.append([(x * MM + y2 * M + z) for x in range(x1, x2) for z in range(z1, z2)])
        if y1 >= 1:
            faces.append([(x * MM + (y1 - 1) * M + z) for x in range(x1, x2) for z in range(z1, z2)])
        if z2 < M:
            faces.append([(x * MM + y * M + z2) for x in range(x1, x2) for y in range(y1, y2)])
        if z1 >= 1:
            faces.append([(x * MM + y * M + z1 - 1) for x in range(x1, x2) for y in range(y1, y2)])
        for f in faces:
            for idx in f:
                g = grid[idx]
                if g >= 0 and g != i:
                    nb.add(g)
        ans[i] = len(nb)
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
