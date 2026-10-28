import sys


def profiles():
    """1D profiles: for offsets (d2, d3) with cube1 at 0, return a dict
    mask -> number of unit cells, mask bit i set iff interval i covers the cell.
    Also keep a representative (a1,a2,a3) start positions."""
    seen = {}
    R = range(-21, 22)
    for d2 in R:
        for d3 in R:
            starts = (0, d2, d3)
            prof = [0] * 8
            for k in range(-30, 30):
                m = 0
                for i, s in enumerate(starts):
                    if s <= k < s + 7:
                        m |= 1 << i
                prof[m] += 1
            key = tuple(prof)
            if key not in seen:
                seen[key] = starts
    return list(seen.items())


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    profs = profiles()
    pc = [bin(i).count("1") for i in range(8)]

    # Combine x and y profiles first, then z.
    xy_list = []
    for px, sx in profs:
        for py, sy in profs:
            vec = [0] * 8
            for mx in range(8):
                if px[mx] == 0:
                    continue
                for my in range(8):
                    if py[my] == 0:
                        continue
                    vec[mx & my] += px[mx] * py[my]
            xy_list.append((tuple(vec), sx, sy))
    # Deduplicate xy vectors
    xy_map = {}
    for vec, sx, sy in xy_list:
        if vec not in xy_map:
            xy_map[vec] = (sx, sy)

    for pz, sz in profs:
        for vec, (sx, sy) in xy_map.items():
            v = [0, 0, 0, 0]
            for m in range(8):
                if vec[m] == 0:
                    continue
                for n in range(8):
                    if pz[n] == 0:
                        continue
                    c = pc[m & n]
                    if c:
                        v[c] += vec[m] * pz[n]
            if v[1] == V1 and v[2] == V2 and v[3] == V3:
                # sx, sy, sz: per-cube start coordinates along each axis
                res = []
                for i in range(3):
                    res.extend([sx[i], sy[i], sz[i]])
                print("Yes")
                print(" ".join(map(str, res)))
                return
    print("No")


main()
