import sys


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    M = int(data[1])
    Ls = [int(x) for x in data[2:2 + 2 * M:2]]
    Rs = [int(x) for x in data[3:3 + 2 * M:2]]
    ops = [0] * M

    def out(cost):
        sys.stdout.write(str(cost) + "\n" + " ".join(map(str, ops)) + "\n")

    # Cost 1: full interval
    for i in range(M):
        if Ls[i] == 1 and Rs[i] == N:
            ops[i] = 1
            out(1)
            return

    # argmax L, argmin R
    p = max(range(M), key=lambda i: Ls[i])
    q = min(range(M), key=lambda i: Rs[i])
    # Cost 2: two disjoint intervals -> two op2
    if Ls[p] > Rs[q]:
        ops[p] = 2
        ops[q] = 2
        out(2)
        return

    # Cost 2: two op1 covering [1,N]
    a = min(range(M), key=lambda i: Ls[i])
    b = max(range(M), key=lambda i: Rs[i])
    if Ls[a] == 1 and Rs[b] == N and a != b:
        ops[a] = 1
        ops[b] = 1
        out(2)
        return

    # Cost 2: some interval strictly contained in another -> op2 on inner, op1 on outer
    order = sorted(range(M), key=lambda i: (Ls[i], -Rs[i]))
    best_R = -1
    best_idx = -1
    for i in order:
        if best_R >= Rs[i]:
            ops[i] = 2
            ops[best_idx] = 1
            out(2)
            return
        if Rs[i] > best_R:
            best_R = Rs[i]
            best_idx = i

    # Cost 3: op2 on p, q (p != q), op1 on any other interval
    if M >= 3:
        r = next(i for i in range(M) if i != p and i != q)
        ops[p] = 2
        ops[q] = 2
        ops[r] = 1
        out(3)
        return

    print(-1)


main()
