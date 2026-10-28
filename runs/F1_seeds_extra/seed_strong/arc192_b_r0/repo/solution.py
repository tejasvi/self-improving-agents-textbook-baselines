import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    k = sum(1 for x in a if int(x) % 2 == 1)
    if n == 1:
        win = True
    elif n == 2:
        win = False
    elif n == 3:
        win = k >= 1
    else:
        win = k % 2 == 1
    print("Fennec" if win else "Snuke")


main()
