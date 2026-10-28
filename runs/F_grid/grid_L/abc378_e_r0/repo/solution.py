import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    a = data[2:2 + n]

    # prefix sums modulo m: r[0..n]
    r = [0] * (n + 1)
    s = 0
    for i in range(n):
        s = (s + int(a[i])) % m
        r[i + 1] = s

    # For pairs i < j (prefix indices 0..n):
    # (S_j - S_i) mod M = r_j - r_i + M * [r_i > r_j]
    # Sum of (r_j - r_i) over pairs: sum_k r_k * (k - (n - k))
    total = 0
    for k in range(n + 1):
        total += r[k] * (2 * k - n)

    # Count pairs i < j with r_i > r_j using a Fenwick tree over values 0..m-1
    tree = [0] * (m + 1)
    inversions = 0
    seen = 0
    for k in range(n + 1):
        v = r[k]
        # count of previous values <= v
        i = v + 1
        c = 0
        while i > 0:
            c += tree[i]
            i -= i & -i
        inversions += seen - c  # previous values strictly greater than v
        i = v + 1
        while i <= m:
            tree[i] += 1
            i += i & -i
        seen += 1

    total += m * inversions
    print(total)


main()
