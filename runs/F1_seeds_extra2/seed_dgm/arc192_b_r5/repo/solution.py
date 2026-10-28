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
        ans = "Fennec" if any(x % 2 == 1 for x in a) else "Snuke"
    else:
        odd = sum(1 for x in a if x % 2 == 1)
        ans = "Snuke" if odd % 2 == 0 else "Fennec"
    print(ans)


main()
