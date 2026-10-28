import sys
from collections import Counter


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    B = [int(x) for x in data[1 + n:1 + 2 * n]]

    # K: known A values (free A slots = m), Bk: known B values (p unknown B slots)
    K = [x for x in A if x != -1]
    Bk = [x for x in B if x != -1]
    k = len(K)
    p = n - len(Bk)
    # Need at least t = k - p known A values matched exactly with S - b for some b in Bk.
    t = k - p
    if t <= 0:
        print("Yes")
        return

    L = max(max(K), max(Bk))
    cK = Counter(K)
    cB = Counter(Bk)

    # M[S] = sum over distinct a, b with a + b = S of min(cK[a], cB[b]) (max matching for sum S)
    M = {}
    get = M.get
    for a, ca in cK.items():
        for b, cb in cB.items():
            s = a + b
            M[s] = get(s, 0) + (ca if ca < cb else cb)

    for s, v in M.items():
        if v >= t and s >= L:
            print("Yes")
            return
    print("No")


main()
