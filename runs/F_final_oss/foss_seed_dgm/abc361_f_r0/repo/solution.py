# Solution for counting distinct perfect powers up to N.
# A number x (1 <= x <= N) is counted if it can be written as a^b with a >= 1,
# b >= 2 (both integers). 1 = 1^b is included.
# The approach:
#   * All perfect squares are counted directly via floor(sqrt(N)).
#   * For exponents b >= 3 we generate a^b (a >= 2) up to N.
#     Those that are perfect squares have already been counted, so we skip them.
#   * The generated numbers are stored in a set to avoid duplicates caused by
#     different (a, b) pairs (e.g., 64 = 2^6 = 4^3 = 8^2).
#   * The final answer is sqrt_count + size_of_set.
# This runs fast because the total amount of generated numbers for b >= 3 is
# at most about 10^6 for N = 10^18.

import sys
import math

def integer_kth_root(n: int, k: int) -> int:
    """Return floor(n ** (1/k)) using integer arithmetic.
    Starts with a float approximation and then corrects it.
    """
    if k == 1:
        return n
    # Initial approximation using float pow (may be slightly off)
    approx = int(n ** (1.0 / k))
    # Ensure approx is not zero
    if approx < 1:
        approx = 1
    # Adjust upwards if (approx+1)^k <= n
    while pow(approx + 1, k) <= n:
        approx += 1
    # Adjust downwards if approx^k > n
    while pow(approx, k) > n:
        approx -= 1
    return approx

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)

    # Count of perfect squares (including 1)
    sqrt_cnt = math.isqrt(N)

    extra = set()
    # Maximum exponent we need to consider (2^b <= N)
    max_b = N.bit_length()  # since 2**(bit_length-1) <= N < 2**bit_length
    # Actually we need b where 2**b <= N, so max_b = floor(log2(N))
    max_b = max_b - 1
    for b in range(3, max_b + 1):
        limit = integer_kth_root(N, b)
        if limit < 2:
            continue
        for a in range(2, limit + 1):
            val = pow(a, b)
            if val > N:
                break
            # Skip if val is a perfect square (already counted)
            if math.isqrt(val) ** 2 == val:
                continue
            extra.add(val)
    ans = sqrt_cnt + len(extra)
    print(ans)

if __name__ == "__main__":
    main()
