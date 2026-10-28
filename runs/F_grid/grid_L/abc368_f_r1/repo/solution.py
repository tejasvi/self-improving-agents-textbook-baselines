import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    m = max(a) if a else 1
    # Omega(k): number of prime factors with multiplicity, via smallest prime factor sieve
    spf = list(range(m + 1))
    i = 2
    while i * i <= m:
        if spf[i] == i:
            for j in range(i * i, m + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    omega = [0] * (m + 1)
    for k in range(2, m + 1):
        omega[k] = omega[k // spf[k]] + 1
    x = 0
    for v in a:
        x ^= omega[v]
    print("Anna" if x else "Bruno")


main()
