# Solution for "Revenge of The Salary of AtCoder Inc."
# Computes the expected total salary modulo 998244353.
# The expectation is derived using dynamic programming from the end state.
# Let E[i] be the expected remaining payout when the current maximum rolled value is i (0 <= i <= N).
# For i = N, E[N] = 0 because no larger roll is possible.
# For i < N, the next roll y is uniformly in [1, N]. If y > i we receive A_y and continue from state y,
# otherwise the process stops. Therefore:
#   E[i] = (1/N) * sum_{y=i+1}^{N} (A_y + E[y])
# Define S[i] = sum_{y=i}^{N} (A_y + E[y]). Then E[i] = (1/N) * S[i+1] and S[i] = (A_i + E[i]) + S[i+1].
# By iterating i from N down to 1 we can compute all values in O(N).
# The answer required is E[0] = (1/N) * S[1].

import sys
MOD = 998244353

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    invN = pow(N, MOD - 2, MOD)  # modular inverse of N
    # S_next corresponds to S[i+1] during the iteration (initially S[N+1] = 0)
    S_next = 0
    # We'll compute E[i] as needed but only keep the running S[i]
    for i in range(N, 0, -1):
        # E[i] = invN * S[i+1]
        Ei = invN * S_next % MOD
        # S[i] = A_i + E[i] + S[i+1]
        Si = (A[i - 1] + Ei + S_next) % MOD
        # Prepare for next iteration (i-1)
        S_next = Si
    # After loop, S_next == S[1]
    answer = invN * S_next % MOD  # E[0]
    print(answer)

if __name__ == "__main__":
    main()
