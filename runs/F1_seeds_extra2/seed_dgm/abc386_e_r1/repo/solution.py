import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    total = 0
    for x in a:
        total ^= x

    # XOR of a K-subset = (XOR of all) ^ (XOR of complement, size N-K).
    # Work with the smaller side m = min(K, N-K); offset = total if complement is used.
    m = min(k, n - k)
    offset = total if k > n - k else 0

    if m == 0:
        print(offset)
        return
    if m == 1:
        # Subsets of size 1 of the (possibly complemented) side: XOR is a single element.
        if k > n - k:
            # complement of size 1: value = total ^ a_i
            best = max(total ^ x for x in a)
        else:
            best = max(a)
        print(best)
        return

    # dp[j] = set of XORs of j-element subsets of the processed prefix.
    # Since m <= N/2 and C(N, m) <= 1e6, these sets stay small when m >= 2.
    dp = [set() for _ in range(m + 1)]
    dp[0].add(0)
    for i, x in enumerate(a):
        for j in range(min(m, i + 1), 0, -1):
            prev = dp[j - 1]
            if prev:
                dp[j].update([v ^ x for v in prev])

    best = 0
    for s in dp[m]:
        v = s ^ offset
        if v > best:
            best = v
    print(best)


main()
