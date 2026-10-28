import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1 + n]
    k = sum(int(x) & 1 for x in a)  # number of odd A_i
    if n == 1:
        winner = "Fennec"
    elif n == 2:
        winner = "Snuke"
    elif n == 3:
        winner = "Snuke" if k == 0 else "Fennec"
    else:
        winner = "Fennec" if k % 2 == 1 else "Snuke"
    print(winner)


if __name__ == "__main__":
    main()
