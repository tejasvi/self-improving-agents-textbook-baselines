import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    odd = sum(int(x) & 1 for x in a)
    if n == 1:
        fennec = True
    elif n == 2:
        fennec = False
    elif n == 3:
        fennec = odd > 0
    else:
        fennec = odd % 2 == 1
    print("Fennec" if fennec else "Snuke")


main()
