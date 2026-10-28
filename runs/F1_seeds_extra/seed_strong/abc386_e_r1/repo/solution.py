import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = 0
    for x in a:
        total ^= x
    # XOR of a K-subset = total ^ XOR of its complement (size N-K).
    # Enumerate the smaller side m = min(K, N-K) subsets.
    if k > n - k:
        m = n - k
        comp = True
    else:
        m = k
        comp = False
    if m == 0:
        print(total if comp else 0)
        return
    # Level-by-level expansion: states are (xor value, next start index).
    # Each state at depth d has a list of xor values with the last index used.
    # We keep two parallel lists: xors and last-used index.
    xs = [0]
    last = [-1]
    for d in range(m):
        remaining = m - d  # elements still to pick including this one
        nxs = []
        nlast = []
        for x, l in zip(xs, last):
            for j in range(l + 1, n - remaining + 1):
                nxs.append(x ^ a[j])
                nlast.append(j)
        xs = nxs
        last = nlast
    if comp:
        ans = max(x ^ total for x in xs)
    else:
        ans = max(xs)
    print(ans)


main()
