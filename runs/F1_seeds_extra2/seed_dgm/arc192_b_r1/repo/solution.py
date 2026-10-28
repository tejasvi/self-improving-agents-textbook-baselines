import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    odd = sum(x & 1 for x in a)
    if n == 1:
        winner = "Fennec"
    elif n == 2:
        winner = "Snuke"
    elif n == 3:
        winner = "Fennec" if odd > 0 else "Snuke"
    else:
        winner = "Fennec" if odd % 2 == 1 else "Snuke"
    print(winner)


main()
