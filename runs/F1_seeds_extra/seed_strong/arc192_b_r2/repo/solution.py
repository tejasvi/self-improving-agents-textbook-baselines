import sys


def solve(n, a):
    if n == 1:
        return "Fennec"
    if n == 2:
        return "Snuke"
    odd = sum(x & 1 for x in a)
    if n == 3:
        return "Snuke" if odd == 0 else "Fennec"
    return "Fennec" if odd % 2 == 1 else "Snuke"


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    print(solve(n, a))


if __name__ == "__main__":
    main()
