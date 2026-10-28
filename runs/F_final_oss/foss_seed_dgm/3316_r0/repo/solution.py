from typing import List
import functools

MOD = 10**9 + 7

class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        """Return the sum of the minimal absolute difference (the *power*) of every
        subsequence of length ``k``.

        The idea is to count, for each possible difference ``D``, how many
        subsequences have *minimum* difference exactly ``D``.  Let

        * ``total`` be the total number of subsequences of size ``k`` (``C(n, k)``).
        * ``g(D)`` be the number of subsequences where *all* pairwise differences are
          **strictly greater** than ``D``.
        * ``f(D) = total - g(D)`` – the number of subsequences whose minimum
          difference is **≤** ``D``.
        * ``cnt(D) = f(D) - f(prev)`` – the number whose minimum difference is
          exactly ``D`` (``prev`` is the previous smaller difference).
        The answer is ``Σ D * cnt(D)``.

        For a fixed ``D`` we can count ``g(D)`` with a DP that builds a subset by
        selecting elements in increasing order and always jumping to the first
        index whose value differs by more than ``D``.  Because ``n ≤ 50`` a simple
        memoised recursion is fast enough.
        """
        n = len(nums)
        if k > n:
            return 0

        # Sort values – the absolute difference between any two elements is
        # simply the difference of their sorted positions.
        a = sorted(nums)

        # ----- combinatorial helpers (modular nCk) -----
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        inv_fact = [1] * (n + 1)
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        def comb(nn: int, rr: int) -> int:
            if rr < 0 or rr > nn:
                return 0
            return fact[nn] * inv_fact[rr] % MOD * inv_fact[nn - rr] % MOD

        total_subsets = comb(n, k)

        # All distinct differences that can appear as a minimum.
        diff_vals = set()
        for i in range(n):
            for j in range(i + 1, n):
                diff_vals.add(a[j] - a[i])
        diff_list = sorted(diff_vals)

        # ---------- helper: count subsets where every pairwise diff > D ----------
        def count_spaced(D: int) -> int:
            # For each position i, find the first index > i whose value differs
            # from a[i] by more than D.  This enables a jump‑ahead DP.
            next_idx = [0] * n
            j = 0
            for i in range(n):
                j = max(j, i + 1)
                while j < n and a[j] - a[i] <= D:
                    j += 1
                next_idx[i] = j

            @functools.lru_cache(maxsize=None)
            def dfs(pos: int, need: int) -> int:
                # Number of ways to pick ``need`` elements from the suffix
                # starting at ``pos`` respecting the spacing constraint.
                if need == 0:
                    return 1
                if pos >= n:
                    return 0
                # Not enough elements left -> 0
                if n - pos < need:
                    return 0
                # Option 1: skip a[pos]
                res = dfs(pos + 1, need)
                # Option 2: take a[pos] and jump to the first allowed index
                res = (res + dfs(next_idx[pos], need - 1)) % MOD
                return res

            return dfs(0, k)

        prev_f = 0  # f(prev) – subsets with min diff ≤ previous D
        answer = 0
        for D in diff_list:
            g = count_spaced(D)  # subsets where all diffs > D
            f = (total_subsets - g) % MOD  # subsets with min diff ≤ D
            cnt_exact = (f - prev_f) % MOD  # subsets where min diff == D
            answer = (answer + (D % MOD) * cnt_exact) % MOD
            prev_f = f

        return answer
