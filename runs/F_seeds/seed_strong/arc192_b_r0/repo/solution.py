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
    if n == 3:
        # Snuke wins iff all A_i - 1 are odd (i.e. all A_i even)
        print("Snuke" if all((x - 1) % 2 == 1 for x in a) else "Fennec")
        return
    s = sum(x - 1 for x in a)
    if n % 2 == 0:
        fennec = (s % 2 == 1)
    else:
        fennec = (s % 2 == 0)
    print("Fennec" if fennec else "Snuke")


main()
