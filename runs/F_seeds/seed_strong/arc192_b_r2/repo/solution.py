import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Snuke" if all(x % 2 == 0 for x in a) else "Fennec"
    else:
        ans = "Snuke" if sum(a) % 2 == 0 else "Fennec"
    print(ans)


main()
