import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()[:3 ** n]

    # c0[i] / c1[i]: min number of changes so that node i evaluates to 0 / 1.
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    cur = s
    for _ in range(n):
        k = len(c0) // 3
        n0 = [0] * k
        n1 = [0] * k
        for i in range(k):
            a, b, c = c0[3 * i], c0[3 * i + 1], c0[3 * i + 2]
            n0[i] = a + b + c - max(a, b, c)  # sum of two cheapest
            a, b, c = c1[3 * i], c1[3 * i + 1], c1[3 * i + 2]
            n1[i] = a + b + c - max(a, b, c)
        c0, c1 = n0, n1
        cur = ''.join('1' if cur[3 * i:3 * i + 3].count('1') >= 2 else '0'
                      for i in range(k))

    # Flipping the root's current value costs the opposite-side cost.
    print(c1[0] if cur == '0' else c0[0])


main()
