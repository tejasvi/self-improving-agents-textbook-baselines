import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    s = s[:m]
    # Root value under the majority reduction.
    vals = [int(c) for c in s]
    for _ in range(n):
        vals = [1 if a + b + c >= 2 else 0
                for a, b, c in zip(vals[0::3], vals[1::3], vals[2::3])]
    cur = vals[0]
    # f0[i] / f1[i]: min number of flips to make node i evaluate to 0 / 1.
    f0 = [0 if c == '0' else 1 for c in s]
    f1 = [0 if c == '1' else 1 for c in s]
    for _ in range(n):
        g0 = []
        g1 = []
        for i in range(0, len(f0), 3):
            a0, b0, c0 = f0[i], f0[i + 1], f0[i + 2]
            a1, b1, c1 = f1[i], f1[i + 1], f1[i + 2]
            # Cheapest 2 of 3 children.
            g0.append(a0 + b0 + c0 - max(a0, b0, c0))
            g1.append(a1 + b1 + c1 - max(a1, b1, c1))
        f0, f1 = g0, g1
    # Flip the root to the opposite of its current value.
    print(f1[0] if cur == 0 else f0[0])


main()
