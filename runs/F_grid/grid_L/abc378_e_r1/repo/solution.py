import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    a = data[2:2 + n]

    # prefix sums mod m, indices 0..n
    r = [0] * (n + 1)
    s = 0
    for i in range(n):
        s += int(a[i])
        r[i + 1] = s % m

    # sum over pairs i<j of (r_j - r_i)  = sum_j r_j * (2j - n)
    total = 0
    for j in range(n + 1):
        total += r[j] * (2 * j - n)

    # count pairs i<j with r_i > r_j using a Fenwick tree over values
    size = m
    tree = [0] * (size + 1)
    inversions = 0
    seen = 0
    for j in range(n + 1):
        v = r[j]
        # count of previous values <= v
        k = v + 1
        c = 0
        while k > 0:
            c += tree[k]
            k -= k & (-k)
        inversions += seen - c
        k = v + 1
        while k <= size:
            tree[k] += 1
            k += k & (-k)
        seen += 1

    print(total + m * inversions)


main()
