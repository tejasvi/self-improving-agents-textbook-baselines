import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    last = {}
    total = 0
    for j in range(1, n + 1):
        v = a[j - 1]
        p = last.get(v, 0)
        total += (j - p) * (n - j + 1)
        last[v] = j
    print(total)


main()
