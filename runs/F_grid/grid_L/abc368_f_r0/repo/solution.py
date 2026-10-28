import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    m = max(a) if a else 1
    # omega[x] = number of prime factors of x counted with multiplicity
    omega = [0] * (m + 1)
    spf = list(range(m + 1))
    i = 2
    while i * i <= m:
        if spf[i] == i:
            for j in range(i * i, m + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    for x in range(2, m + 1):
        omega[x] = omega[x // spf[x]] + 1
    g = 0
    for v in a:
        g ^= omega[v]
    print("Anna" if g != 0 else "Bruno")


main()
