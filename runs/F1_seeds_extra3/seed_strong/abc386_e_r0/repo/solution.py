import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = 0
    for x in a:
        total ^= x
    # XOR of K-subset = total ^ XOR of complement (size N-K)
    m = min(k, n - k)
    complement = (m != k)
    # sets[j] = set of XORs of j-subsets among processed elements
    sets = [set() for _ in range(m + 1)]
    sets[0].add(0)
    for i, x in enumerate(a):
        # only j in [max(1, m-(n-1-i)) .. min(m, i+1)] matter, but full update is fine
        hi = min(m, i + 1)
        for j in range(hi, 0, -1):
            prev = sets[j - 1]
            if not prev:
                continue
            cur = sets[j]
            cur.update([y ^ x for y in prev])
    best = 0
    if complement:
        for v in sets[m]:
            t = v ^ total
            if t > best:
                best = t
    else:
        for v in sets[m]:
            if v > best:
                best = v
    print(best)


main()
