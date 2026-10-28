import sys

def main():
    V1, V2, V3 = map(int, sys.stdin.read().split())
    S = 7
    if V1 + 2 * V2 + 3 * V3 != 3 * S**3:
        print("No")
        return
    # 1D patterns: cubes at 0, p, q with length S intervals
    def ov(*iv):
        lo = max(x[0] for x in iv)
        hi = min(x[1] for x in iv)
        return max(0, hi - lo)
    R = range(-2 * S - 1, 2 * S + 2)
    reps = {}
    for p in R:
        for q in R:
            A = (0, S); B = (p, p + S); C = (q, q + S)
            key = (ov(A, B, C), ov(A, B), ov(A, C), ov(B, C))
            if key not in reps:
                reps[key] = (p, q)
    keys = list(reps.keys())
    # Need product over dims: T = prod t_i = V3, P = sum_pairs prod l_ij = V2 + 3*V3
    target_P = V2 + 3 * V3
    for k0 in keys:
        t0, a0, b0, c0 = k0
        for k1 in keys:
            t1, a1, b1, c1 = k1
            for k2 in keys:
                t2, a2, b2, c2 = k2
                if t0 * t1 * t2 != V3:
                    continue
                P = a0*a1*a2 + b0*b1*b2 + c0*c1*c2
                # pairwise volume of cubes 1&2: product of a_i; 1&3: b_i; 2&3: c_i
                # sum of pairwise volumes = (a0*a1*a2) + (b...) + (c...)
                if P == target_P:
                    p = [reps[k0][0], reps[k1][0], reps[k2][0]]
                    q = [reps[k0][1], reps[k1][1], reps[k2][1]]
                    print("Yes")
                    print(0, 0, 0, p[0], p[1], p[2], q[0], q[1], q[2])
                    return
    print("No")

main()
