# Solution for ABC Puzzle problem.
# The task: construct an N x N grid (N <= 5) with characters A, B, C (or empty) such that:
#   * each row contains exactly one A, one B, one C (others empty)
#   * each column contains exactly one A, one B, one C (others empty)
#   * the leftmost non‑empty cell of row i equals R[i]
#   * the topmost non‑empty cell of column j equals C[j]
#
# Observation:
#   For each symbol X in {A,B,C} we can view the positions of X as a permutation of the columns:
#   π_X[i] = column where X appears in row i.
#   Because each row must contain exactly one X and each column must contain exactly one X,
#   π_X is a bijection (a permutation of 0..N-1).
#   The three permutations must be pairwise column‑wise distinct, i.e. for every row i the three values
#   π_A[i], π_B[i], π_C[i] are all different (otherwise a cell would contain two symbols).
#   The column condition (one of each symbol per column) is automatically satisfied by the bijectivity.
#
#   With the permutations fixed we can recover the whole grid and test the "leftmost" and "topmost"
#   requirements:
#     * For row i the smallest of the three columns determines the leftmost symbol.
#     * For column j we look at the three rows where A, B, C appear in that column; the smallest row index
#       determines the topmost symbol.
#
#   N ≤ 5, so N! ≤ 120.  Enumerating all triples of permutations is at most 120³ ≈ 1.7 million – easily fast.
#   Simple pruning (checking distinctness per row) reduces the search dramatically.
#
# The algorithm enumerates permutations for A, then for B (skipping rows where B would clash with A),
# then for C (skipping rows where C would clash with A or B).  For each complete triple we verify the
#   leftmost and topmost constraints.  The first valid triple yields a solution which we output.
# If no triple works we output "No".
#
# Complexity: O(N!³ * N) which is trivial for N ≤ 5.

import sys
import itertools

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    R = data[1].strip()
    C = data[2].strip()
    # Convert to list for easy indexing (0‑based)
    R_list = list(R)
    C_list = list(C)

    cols = list(range(N))
    # Pre‑generate all permutations of columns
    all_perms = list(itertools.permutations(cols))  # each is a tuple of length N

    # Helper to test a full triple of permutations
    def test_triple(permA, permB, permC) -> bool:
        # Row‑wise distinctness already guaranteed by caller, but verify quickly
        for i in range(N):
            if len({permA[i], permB[i], permC[i]}) != 3:
                return False
        # Leftmost condition per row
        for i in range(N):
            # Determine which symbol is leftmost in this row
            col_vals = [(permA[i], 'A'), (permB[i], 'B'), (permC[i], 'C')]
            col_vals.sort(key=lambda x: x[0])
            left_sym = col_vals[0][1]
            if left_sym != R_list[i]:
                return False
        # Topmost condition per column
        # Build reverse mapping: for each column, which row contains each symbol
        row_of_A = [0] * N
        row_of_B = [0] * N
        row_of_C = [0] * N
        for i in range(N):
            row_of_A[permA[i]] = i
            row_of_B[permB[i]] = i
            row_of_C[permC[i]] = i
        for j in range(N):
            # smallest row index among the three symbols for this column
            candidates = [(row_of_A[j], 'A'), (row_of_B[j], 'B'), (row_of_C[j], 'C')]
            candidates.sort(key=lambda x: x[0])
            top_sym = candidates[0][1]
            if top_sym != C_list[j]:
                return False
        return True

    # Build the grid from a valid triple for output
    def build_grid(permA, permB, permC):
        grid = [['.' for _ in range(N)] for _ in range(N)]
        for i in range(N):
            grid[i][permA[i]] = 'A'
            grid[i][permB[i]] = 'B'
            grid[i][permC[i]] = 'C'
        return [''.join(row) for row in grid]

    # Enumerate triples with pruning
    for permA in all_perms:
        # Quick check: leftmost condition for rows where A would be leftmost alone is not sufficient yet.
        for permB in all_perms:
            # Row distinctness between A and B
            ok = True
            for i in range(N):
                if permB[i] == permA[i]:
                    ok = False
                    break
            if not ok:
                continue
            for permC in all_perms:
                # Row distinctness among three
                ok = True
                for i in range(N):
                    if permC[i] == permA[i] or permC[i] == permB[i]:
                        ok = False
                        break
                if not ok:
                    continue
                if test_triple(permA, permB, permC):
                    grid_lines = build_grid(permA, permB, permC)
                    print('Yes')
                    for line in grid_lines:
                        print(line)
                    return
    # No configuration found
    print('No')

if __name__ == "__main__":
    solve()
