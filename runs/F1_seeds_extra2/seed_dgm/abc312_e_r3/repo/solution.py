import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = 101
    # Flat index of unit cell (yy, zz) on plane `plane` perpendicular to axis a:
    #   ((a*S + plane)*S + yy)*S + zz
    # minOwn[cell] = id of cuboid whose min face lies on that cell; maxOwn likewise for max face.
    SIZE = 3 * S * S * S
    minOwn = [0] * SIZE
    maxOwn = [0] * SIZE
    boxes = []
    pos = 1
    for i in range(n):
        x1, y1, z1, x2, y2, z2 = (int(v) for v in data[pos:pos + 6])
        pos += 6
        boxes.append((x1, y1, z1, x2, y2, z2))
        idx = i + 1
        lo = (x1, y1, z1)
        hi = (x2, y2, z2)
        for a in range(3):
            b, c = [t for t in range(3) if t != a]
            base_min = (a * S + lo[a]) * S
            base_max = (a * S + hi[a]) * S
            for yy in range(lo[b], hi[b]):
                row_min = (base_min + yy) * S
                row_max = (base_max + yy) * S
                for zz in range(lo[c], hi[c]):
                    minOwn[row_min + zz] = idx
                    maxOwn[row_max + zz] = idx

    ans = []
    for i in range(n):
        x1, y1, z1, x2, y2, z2 = boxes[i]
        idx = i + 1
        lo = (x1, y1, z1)
        hi = (x2, y2, z2)
        neigh = set()
        for a in range(3):
            b, c = [t for t in range(3) if t != a]
            base_hi = (a * S + hi[a]) * S
            base_lo = (a * S + lo[a]) * S
            for yy in range(lo[b], hi[b]):
                row_hi = (base_hi + yy) * S
                row_lo = (base_lo + yy) * S
                for zz in range(lo[c], hi[c]):
                    # Our max face touching another's min face (other lies beyond us on axis a)
                    neigh.add(minOwn[row_hi + zz])
                    # Our min face touching another's max face
                    neigh.add(maxOwn[row_lo + zz])
        neigh.discard(0)
        neigh.discard(idx)
        ans.append(len(neigh))
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
