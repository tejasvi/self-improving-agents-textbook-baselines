import sys
from itertools import product

def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    if V1 + 2 * V2 + 3 * V3 != 3 * 343:
        print("No")
        return
    # 1D placements: positions (0, p, q) with p, q in [-14, 14]
    # cell t (unit [t,t+1]) is covered by cube i iff x_i <= t < x_i + 7
    vec_map = {}
    for p in range(-14, 15):
        for q in range(-14, 15):
            xs = (0, p, q)
            cnt = [0] * 8
            for t in range(-30, 30):
                m = 0
                for i in range(3):
                    if xs[i] <= t < xs[i] + 7:
                        m |= 1 << i
                cnt[m] += 1
            key = tuple(cnt)
            if key not in vec_map:
                vec_map[key] = xs
    keys = list(vec_map.keys())
    # Pair combination: 2D vector over masks
    def combine(A, B):
        R = [0] * 8
        for ma in range(8):
            if A[ma]:
                for mb in range(8):
                    if B[mb]:
                        R[ma & mb] += A[ma] * B[mb]
        return tuple(R)
    pair_map = {}
    for i, A in enumerate(keys):
        for B in keys:
            R = combine(A, B)
            if R not in pair_map:
                pair_map[R] = (A, B)
    pkeys = list(pair_map.keys())
    nzk = [[(m, c) for m, c in enumerate(C) if c] for C in keys]
    for P in pkeys:
        nzp = [(m, c) for m, c in enumerate(P) if c]
        for ci, C in enumerate(keys):
            R = [0] * 8
            for ma, pa in nzp:
                for mb, cb in nzk[ci]:
                    R[ma & mb] += pa * cb
            v1 = R[1] + R[2] + R[4]
            v2 = R[3] + R[5] + R[6]
            v3 = R[7]
            if v1 == V1 and v2 == V2 and v3 == V3:
                C = keys[ci]
                A, B = pair_map[P]
                xa = vec_map[A]; xb = vec_map[B]; xc = vec_map[C]
                # Cell-count vectors are per axis: X index, Y index, Z index
                # Build the cube positions: axis x uses xa, y uses xb, z uses xc
                # cube i = (xa[i], xb[i], xc[i])
                out = []
                for i in range(3):
                    out.append(xa[i]); out.append(xb[i]); out.append(xc[i])
                print("Yes")
                print(" ".join(map(str, out)))
                return
    print("No")

main()
