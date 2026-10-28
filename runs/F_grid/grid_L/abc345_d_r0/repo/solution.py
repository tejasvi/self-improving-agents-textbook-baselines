import sys


def main():
    data = sys.stdin.read().split()
    n, h, w = int(data[0]), int(data[1]), int(data[2])
    tiles = []
    for i in range(n):
        a = int(data[3 + 2 * i])
        b = int(data[4 + 2 * i])
        tiles.append((a, b))
    total = h * w
    full = (1 << total) - 1

    def rect_mask(r, c, rh, rw):
        m = 0
        for i in range(rh):
            base = (r + i) * w + c
            m |= ((1 << rw) - 1) << base
        return m

    def fill(grid, used_tiles):
        # grid: bitmask of covered cells; used_tiles: list of tile indices still available
        if grid == full:
            return True
        # first empty cell (lowest zero bit)
        inv = ~grid & full
        low = inv & -inv
        pos = low.bit_length() - 1
        r, c = divmod(pos, w)
        for idx in range(len(used_tiles)):
            t = used_tiles[idx]
            rest = used_tiles[:idx] + used_tiles[idx + 1:]
            a, b = tiles[t]
            orients = {(a, b), (b, a)}
            for rh, rw in orients:
                if r + rh > h or c + rw > w:
                    continue
                m = rect_mask(r, c, rh, rw)
                if grid & m:
                    continue
                if fill(grid | m, rest):
                    return True
        return False

    for s in range(1, 1 << n):
        area = 0
        chosen = []
        for i in range(n):
            if s >> i & 1:
                area += tiles[i][0] * tiles[i][1]
                chosen.append(i)
        if area != total:
            continue
        if fill(0, chosen):
            print("Yes")
            return
    print("No")


main()
