# Solution for the Adjacent GCD problem.
# For each prefix length m, we need the sum over all non‑empty subsequences of the first m
# elements of the score defined as the sum of gcds of adjacent elements in the subsequence.
# The contribution of a pair (i, j) (i < j) to the answer for prefix m (where j ≤ m) is:
#   gcd(A_i, A_j) * 2^{i-1} * 2^{m-j}
# because we may freely choose any subset before i and after j, but must not choose any element
# between i and j. Hence, when extending the prefix from m-1 to m we have the recurrence:
#   ans_m = 2 * ans_{m-1} + sum_{i=1}^{m-1} gcd(A_i, A_m) * 2^{i-1}
# The first term doubles the contributions of all previous pairs (the factor 2 comes from the
# extra choice of whether to include each element after the second element of the pair).
# The second term adds the contributions of the new pairs that end at position m.
#
# To compute the added term efficiently we use the classic identity:
#   sum_{i} gcd(A_i, x) = \sum_{d|x} phi(d) * cnt[d]
# where cnt[d] = sum_{i : d | A_i} 2^{i-1} (the weighted count of indices whose value is a multiple
# of d) and phi is Euler's totient function. Both phi and the list of divisors for every value up
# to max(A) are pre‑computed.
#
# Complexity: O(N \log MAX_A) after preprocessing divisors, easily fast for N ≤ 5·10^5 and
# MAX_A ≤ 10^5.

import sys

MOD = 998244353

def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    max_a = max(a)

    # ---------- pre‑compute Euler's totient up to max_a ----------
    phi = list(range(max_a + 1))
    for i in range(2, max_a + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, max_a + 1, i):
                phi[j] -= phi[j] // i

    # ---------- pre‑compute divisor lists for every number up to max_a ----------
    divisors = [[] for _ in range(max_a + 1)]
    for d in range(1, max_a + 1):
        for multiple in range(d, max_a + 1, d):
            divisors[multiple].append(d)

    # ---------- powers of two (2^{i}) modulo MOD ----------
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    # cnt[d] = sum_{idx processed, d|A_idx} 2^{idx-1}
    cnt = [0] * (max_a + 1)

    ans = 0
    out = []
    for m in range(1, n + 1):
        if m == 1:
            ans = 0
        else:
            # double previous answer
            ans = (ans * 2) % MOD
            x = a[m - 1]
            # sum_{i < m} gcd(A_i, x) * 2^{i-1}
            add = 0
            for d in divisors[x]:
                add = (add + phi[d] * cnt[d]) % MOD
            ans = (ans + add) % MOD
        out.append(str(ans))

        # update cnt for future steps with current element weighted by 2^{m-1}
        weight = pow2[m - 1]
        x = a[m - 1]
        for d in divisors[x]:
            cnt[d] = (cnt[d] + weight) % MOD

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
