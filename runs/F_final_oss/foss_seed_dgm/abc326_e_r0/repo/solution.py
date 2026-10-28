# Solution for "Revenge of The Salary of AtCoder Inc."
# Computes expected total salary modulo 998244353.
# The process can be described by the DP:
#   E[x] = (1/N) * sum_{y=x+1..N} (A_y + E[y]),   for 0 <= x < N
#   E[N] = 0
# We evaluate from high to low, maintaining a suffix sum of (A_y + E[y]).
# The answer is E[0].

import sys

MOD = 998244353

def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0] + [int(next(it)) for _ in range(N)]  # 1-indexed
    invN = pow(N, MOD - 2, MOD)  # modular inverse of N (MOD is prime)

    suffix = 0  # sum_{y = x+1 .. N} (A_y + E[y]) for current x
    answer = 0
    # iterate x from N down to 0
    for x in range(N, -1, -1):
        if x == N:
            E = 0
        else:
            E = suffix * invN % MOD
        if x == 0:
            answer = E
        if x >= 1:
            term = (A[x] + E) % MOD
            suffix = (suffix + term) % MOD
    print(answer)

if __name__ == "__main__":
    main()
