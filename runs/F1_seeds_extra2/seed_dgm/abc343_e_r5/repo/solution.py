import sys


def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    S = 343
    R = 7
    if V1 + 2 * V2 + 3 * V3 != 3 * S:
        print("No")
        return

    # Per-axis tuple for offsets (0, x2, x3):
    # (triple overlap, pair overlap 1-2, pair 1-3, pair 2-3)
    tuples = {}
    for x2 in range(-R, R + 1):
        for x3 in range(-R, R + 1):
            xs = (0, x2, x3)
            t = max(0, R - (max(xs) - min(xs)))
            p12 = max(0, R - abs(x2))
            p13 = max(0, R - abs(x3))
            p23 = max(0, R - abs(x2 - x3))
            key = (t, p12, p13, p23)
            if key not in tuples:
                tuples[key] = (x2, x3)
    keys = list(tuples.keys())

    target = V2 + 3 * V3  # sum of pairwise volumes must equal V2 + 3*V3
    n = len(keys)
    for i in range(n):
        A = keys[i]
        for j in range(i, n):
            B = keys[j]
            for k in range(j, n):
                C = keys[k]
                if A[0] * B[0] * C[0] != V3:
                    continue
                if A[1] * B[1] * C[1] + A[2] * B[2] * C[2] + A[3] * B[3] * C[3] != target:
                    continue
                oA, oB, oC = tuples[A], tuples[B], tuples[C]
                a = [0, oA[0], oA[1]]
                b = [0, oB[0], oB[1]]
                c = [0, oC[0], oC[1]]
                print("Yes")
                print(a[0], b[0], c[0], a[1], b[1], c[1], a[2], b[2], c[2])
                return
    print("No")


main()
