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
        ans = "Fennec" if any(x % 2 for x in a) else "Snuke"
    else:
        odd = sum(x % 2 for x in a)
        ans = "Fennec" if odd % 2 == 1 else "Snuke"
    print(ans)


main()
