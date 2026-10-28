# Solution for Palindromic Expression problem
# We need to output a palindrome string consisting of digits 1-9 and '*',
# whose evaluated value equals N (1 <= N <= 1e12).
# The expression itself must be a palindrome, first character a digit, and length <= 1000.
# The expression can be a single palindrome number, or a symmetric product like
#   a1*a2*...*ak * m * ak*...*a2*a1   (k >= 0, m optional palindrome)
# which corresponds to N = (A)^2 * M where A = product of the left factors, M is a palindrome (or 1).
# All individual factors a_i and the middle factor M must be palindromes without digit '0'.
# We search for such a decomposition using DFS over palindrome factors (up to sqrt(N)).

import sys, math
from typing import List

# ---------- utility functions ----------

def is_pal_nozero(s: str) -> bool:
    """Return True if s is a palindrome and contains no '0'."""
    return '0' not in s and s == s[::-1]

def generate_palindromes(limit: int) -> List[int]:
    """Return a list of all palindrome numbers (digits 1-9 only) <= limit.
    The list is sorted increasingly.
    """
    digits = ['1','2','3','4','5','6','7','8','9']
    pals = []
    max_len = len(str(limit))
    for length in range(1, max_len + 1):
        half = (length + 1) // 2
        def backtrack(pos: int, cur: str):
            if pos == half:
                if length % 2 == 0:
                    pal = cur + cur[::-1]
                else:
                    pal = cur + cur[-2::-1]
                val = int(pal)
                if val <= limit:
                    pals.append(val)
                return
            for d in digits:
                backtrack(pos + 1, cur + d)
        backtrack(0, "")
    pals.sort()
    return pals

def construct_expression(left: List[int], middle: int) -> str:
    """Build the palindrome expression string from left factors and middle factor.
    The pattern is left ... middle ... reversed(left) with '*' separators.
    """
    parts = []
    for a in left:
        parts.append(str(a))
    if middle != 1:  # middle factor 1 would be unnecessary; we skip it to keep length short
        parts.append(str(middle))
    for a in reversed(left):
        parts.append(str(a))
    return '*'.join(parts)

# ---------- main solving routine ----------

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    # 1. Single number case
    if is_pal_nozero(str(N)):
        print(N)
        return

    limit = int(math.isqrt(N))
    # generate palindrome factors up to limit, exclude 1 to avoid infinite loops in DFS
    pal_factors = [p for p in generate_palindromes(limit) if p != 1]

    found = False
    answer = None

    # Depth‑first search over left side factors (allow repetitions, non‑decreasing order)
    # We explore all products <= limit.
    def dfs(start_idx: int, prod: int, left_factors: List[int]):
        nonlocal found, answer
        if found:
            return
        # Check current decomposition
        sq = prod * prod
        if N % sq == 0:
            middle = N // sq
            if is_pal_nozero(str(middle)):
                expr = construct_expression(left_factors, middle)
                if len(expr) <= 1000:
                    answer = expr
                    found = True
                    return
        # Try adding another factor
        for i in range(start_idx, len(pal_factors)):
            a = pal_factors[i]
            new_prod = prod * a
            if new_prod > limit:
                break
            dfs(i, new_prod, left_factors + [a])
            if found:
                return

    dfs(0, 1, [])

    if found:
        print(answer)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
