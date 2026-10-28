# Solution for "Revenge of \"The Salary of AtCoder Inc.\""
# Implements the expected salary computation modulo 998244353.
# The process is modeled with DP: E[x] = (1/N) * sum_{y=x+1..N} (A_y + E[y])
# Compute backwards using cumulative suffix sums.

import sys

MOD = 998244353

def main() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A_list = [int(next(it)) for _ in range(N)]
    # 1-indexed array for convenience; A[0] = 0
    A = [0] + A_list
    invN = pow(N, MOD - 2, MOD)  # modular inverse of N
    E = [0] * (N + 1)  # E[x] for x = 0..N
    suffix = 0  # sum_{y=x+1..N} (A[y] + E[y]) for current x
    for x in range(N, -1, -1):
        # Expected value from state x
        E[x] = suffix * invN % MOD
        # Prepare suffix for next iteration (x-1)
        B = (A[x] + E[x]) % MOD
        suffix = (suffix + B) % MOD
    print(E[0] % MOD)

if __name__ == "__main__":
    main()
