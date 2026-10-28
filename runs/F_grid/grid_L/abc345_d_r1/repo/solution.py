import sys


def main():
    data = sys.stdin.read().split()
    n, h, w = int(data[0]), int(data[1]), int(data[2])
    tiles = []
    for i in range(n):
        a, b = int(data[3 + 2 * i]), int(data[4 + 2 * i])
        tiles.append((a, b))
    full = (1 << (h * w)) - 1

    # Precompute rectangle masks per (r, c, height, width) lazily.
    rect_cache = {}

    def rect_mask(r, c, rh, rw):
        key = (r, c, rh, rw)
        m = rect_cache.get(key)
        if m is None:
            m = 0
            for i in range(rh):
                for j in range(rw):
                    m |= 1 << ((r + i) * w + (c + j))
            rect_cache[key] = m
        return m

    def solve(subset):
        # subset: list of tile indices; total area == h*w assumed
        k = len(subset)
        failed = set()

        def dfs(grid, used):
            if grid == full:
                return True
            key = (grid, used)
            if key in failed:
                return False
            # first empty cell
            inv = ~grid & full
            p = (inv & -inv).bit_length() - 1
            r, c = divmod(p, w)
            for idx in range(k):
                if used >> idx & 1:
                    continue
                a, b = tiles[subset[idx]]
                orients = {(a, b), (b, a)}
                for (rh, rw) in orients:
                    if r + rh > h or c + rw > w:
                        continue
                    m = rect_mask(r, c, rh, rw)
                    if grid & m:
                        continue
                    if dfs(grid | m, used | (1 << idx)):
                        return True
            failed.add(key)
            return False

        return dfs(0, 0)

    target = h * w
    for s in range(1, 1 << n):
        idxs = [i for i in range(n) if s >> i & 1]
        area = sum(tiles[i][0] * tiles[i][1] for i in idxs)
        if area != target:
            continue
        if solve(idxs):
            print("Yes")
            return
    print("No")


main()
