import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    if n == 1:
        print("Fennec")
        return
    if n == 2:
        print("Snuke")
        return
    odd = sum(x & 1 for x in a)
    if n == 3:
        print("Snuke" if odd == 0 else "Fennec")
        return
    print("Snuke" if odd % 2 == 0 else "Fennec")


main()
