import sys


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    # XOR of a K-subset S = T ^ XOR(complement of S), |complement| = N-K.
    # Enumerate XORs of subsets of size m = min(K, N-K).
    m = min(k, n - k)
    total = 0
    for x in a:
        total ^= x

    # dp[j] = set of XOR values over j-subsets of processed elements
    dp = [set() for _ in range(m + 1)]
    dp[0].add(0)
    for i, x in enumerate(a):
        for j in range(min(m, i + 1), 0, -1):
            prev = dp[j - 1]
            if prev:
                dp[j].update([v ^ x for v in prev])

    vals = dp[m]
    if k <= n - k:
        ans = max(vals)
    else:
        ans = max(v ^ total for v in vals)
    print(ans)


if __name__ == "__main__":
    main()
