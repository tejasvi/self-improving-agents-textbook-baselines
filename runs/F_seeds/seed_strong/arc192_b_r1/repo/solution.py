import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    if n == 1:
        print("Fennec")
        return
    if n == 2:
        print("Snuke")
        return
    odd = sum(int(x) & 1 for x in a)
    if n == 3:
        # Snuke wins only if every value is even
        print("Snuke" if odd == 0 else "Fennec")
        return
    print("Snuke" if odd % 2 == 0 else "Fennec")


main()
