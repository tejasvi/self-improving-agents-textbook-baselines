import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    G = 102  # coordinates shifted by +1 so that padding cells (0) surround the grid
    GG = G * G
    own = [0] * (G * GG)
    boxes = []
    p = 1
    for i in range(n):
        x1, y1, z1, x2, y2, z2 = (int(v) for v in data[p:p + 6])
        p += 6
        boxes.append((x1, y1, z1, x2, y2, z2))
        tag = i + 1
        dz = z2 - z1
        for x in range(x1 + 1, x2 + 1):
            for y in range(y1 + 1, y2 + 1):
                b = x * GG + y * G + z1 + 1
                own[b:b + dz] = [tag] * dz

    pairs = set()
    for i in range(n):
        x1, y1, z1, x2, y2, z2 = boxes[i]
        tag = i + 1
        dz = z2 - z1
        # Neighbour planes: x = x2 (cell x2), x = x1-1 (cell x1-1), similarly y, z.
        # Shifted indices: cell c -> c+1.
        # X faces
        for xp in (x2 + 1, x1):  # shifted index of neighbour cell
            for y in range(y1 + 1, y2 + 1):
                b = xp * GG + y * G + z1 + 1
                for j in set(own[b:b + dz]):
                    if j and j != tag:
                        pairs.add((j, tag) if j < tag else (tag, j))
        # Y faces
        for yp in (y2 + 1, y1):
            for x in range(x1 + 1, x2 + 1):
                b = x * GG + yp * G + z1 + 1
                for j in set(own[b:b + dz]):
                    if j and j != tag:
                        pairs.add((j, tag) if j < tag else (tag, j))
        # Z faces
        for zp in (z2 + 1, z1):
            for x in range(x1 + 1, x2 + 1):
                for y in range(y1 + 1, y2 + 1):
                    j = own[x * GG + y * G + zp]
                    if j and j != tag:
                        pairs.add((j, tag) if j < tag else (tag, j))

    deg = [0] * (n + 1)
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    sys.stdout.write("\n".join(map(str, deg[1:])) + "\n")


main()
