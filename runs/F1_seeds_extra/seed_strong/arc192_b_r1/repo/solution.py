import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    if n == 1:
        win = True
    elif n == 2:
        win = False
    elif n == 3:
        win = any(x % 2 == 1 for x in a)
    else:
        win = sum(x % 2 for x in a) % 2 == 1
    print("Fennec" if win else "Snuke")


main()
