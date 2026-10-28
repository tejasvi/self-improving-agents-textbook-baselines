import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    idx = 1
    for _ in range(n):
        vals = [int(v) for v in data[idx:idx + 6]]
        idx += 6
        cubes.append((vals[0:3], vals[3:6]))

    S = 101
    SIZE = S * S * S
    neighbors = [set() for _ in range(n)]

    for a in range(3):
        b, c = [k for k in range(3) if k != a]
        for side in range(2):
            # side 0: owners keyed by low face of j, queried by high face of i
            # side 1: owners keyed by high face of j, queried by low face of i
            owner = [-1] * SIZE
            for j in range(n):
                lo, hi = cubes[j]
                plane = lo[a] if side == 0 else hi[a]
                base = plane * S * S
                for u in range(lo[b], hi[b]):
                    row = base + u * S
                    for v in range(lo[c], hi[c]):
                        owner[row + v] = j
            for i in range(n):
                lo, hi = cubes[i]
                plane = hi[a] if side == 0 else lo[a]
                base = plane * S * S
                found = neighbors[i]
                for u in range(lo[b], hi[b]):
                    row = base + u * S
                    for v in range(lo[c], hi[c]):
                        j = owner[row + v]
                        if j >= 0 and j != i:
                            found.add(j)

    sys.stdout.write("\n".join(str(len(s)) for s in neighbors) + "\n")


main()
