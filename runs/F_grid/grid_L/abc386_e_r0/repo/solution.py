import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    K = int(data[1])
    A = [int(x) for x in data[2:2 + n]]

    T = 0
    for a in A:
        T ^= a

    # XOR of a K-subset = T ^ XOR of its complement (size N-K).
    # So we can work with k = min(K, N-K).
    use_complement = (n - K) < K
    k = min(K, n - K)

    # sets[j] = distinct XORs of j-subsets of the prefix processed so far
    sets = [set() for _ in range(k + 1)]
    sets[0].add(0)

    for a in A:
        for j in range(k, 0, -1):
            prev = sets[j - 1]
            if not prev:
                continue
            cur = sets[j]
            for x in prev:
                cur.add(x ^ a)

    best = 0
    for x in sets[k]:
        v = (x ^ T) if use_complement else x
        if v > best:
            best = v
    print(best)


main()
