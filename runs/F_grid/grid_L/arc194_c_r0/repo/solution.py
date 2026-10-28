import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]
    C = list(map(int, data[1 + 2 * n:1 + 3 * n]))

    W0 = 0
    for k in range(n):
        if A[k] == b'1':
            W0 += C[k]

    # Unique ranks (1-based) by (C, index) for BIT indexing.
    order = sorted(range(n), key=lambda k: (C[k], k))
    rank = [0] * n
    for pos, k in enumerate(order):
        rank[k] = pos + 1

    size = n + 1
    cntN = [0] * (size + 1)
    sumN = [0] * (size + 1)
    cntP = [0] * (size + 1)
    sumP = [0] * (size + 1)

    def bit_add(tree, i, v):
        while i <= size:
            tree[i] += v
            i += i & -i

    def bit_query(tree, i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    # State of the two multisets:
    #   N: flipped 1->0 (mismatched, plus temporarily-lowered matched ones)
    #   P: flipped 0->1 (mismatched, plus temporarily-lowered matched ones)
    nN = nP = 0
    SN = SP = 0
    pN = pP = 0  # sum over unordered pairs of max value

    def insert_N(k):
        nonlocal nN, SN, pN
        x = C[k]
        r = rank[k]
        less_cnt = bit_query(cntN, r - 1)
        less_sum = bit_query(sumN, r - 1)
        greater_sum = SN - less_sum
        pN += x * less_cnt + greater_sum
        bit_add(cntN, r, 1)
        bit_add(sumN, r, x)
        nN += 1
        SN += x

    def insert_P(k):
        nonlocal nP, SP, pP
        x = C[k]
        r = rank[k]
        less_cnt = bit_query(cntP, r - 1)
        less_sum = bit_query(sumP, r - 1)
        greater_sum = SP - less_sum
        pP += x * less_cnt + greater_sum
        bit_add(cntP, r, 1)
        bit_add(sumP, r, x)
        nP += 1
        SP += x

    matched_one = []
    for k in range(n):
        a = A[k]
        b = B[k]
        if a == b'1' and b == b'0':
            insert_N(k)
        elif a == b'0' and b == b'1':
            insert_P(k)
        elif a == b'1' and b == b'1':
            matched_one.append(k)

    # Temporarily lowering the largest matched-1 positions is optimal (prefix by C desc).
    matched_one.sort(key=lambda k: -C[k])

    def evaluate():
        T = nN + nP
        return T * W0 - (1 + nP) * SN - pN + nP * SP - pP

    best = evaluate()
    for k in matched_one:
        insert_N(k)
        insert_P(k)
        val = evaluate()
        if val < best:
            best = val
    print(best)


main()
