import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    total = 0
    for x in a:
        total ^= x

    # XOR of a K-subset == total ^ XOR of its complement (size N-K).
    # Enumerate the smaller side m = min(K, N-K), which is small by constraints.
    complement = k > n - k
    m = n - k if complement else k

    if m == 0:
        print(total)
        return

    a.sort()
    best = -1

    # DFS over index combinations; the last level is a max over a slice.
    def rec(start, depth, cur):
        nonlocal best
        if depth == m - 1:
            # choose the last element from a[start:]
            v = max(cur ^ x for x in a[start:])
            if v > best:
                best = v
            return
        for i in range(start, n - (m - depth) + 1):
            rec(i + 1, depth + 1, cur ^ a[i])

    # complement case: K-subset XOR = total ^ (complement XOR), so seed with total
    rec(0, 0, total if complement else 0)

    print(best)


main()
