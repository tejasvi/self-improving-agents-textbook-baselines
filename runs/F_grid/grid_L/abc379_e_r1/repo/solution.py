import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    cur = 0  # sum of f(j, i) over all j <= i
    total = 0
    for i in range(1, n + 1):
        d = ord(s[i - 1]) - 48
        cur = cur * 10 + d * i
        total += cur
    print(total)


if __name__ == "__main__":
    main()
