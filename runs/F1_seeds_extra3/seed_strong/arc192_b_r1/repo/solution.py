import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    p = sum(1 for x in a if int(x) % 2 == 1)
    if n == 1:
        ans = True
    elif n == 2:
        ans = False
    elif n == 3:
        ans = p >= 1
    else:
        ans = p % 2 == 1
    print("Fennec" if ans else "Snuke")


main()
