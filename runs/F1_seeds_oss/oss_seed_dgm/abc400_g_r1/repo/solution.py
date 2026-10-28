# Solution for AtCoder ABC 400 Patisserie ABC 3
# We implement the greedy algorithm described in the editorial.
# For each cake we take its maximum attribute value and the dimension (0,1,2) where it occurs.
# We select the 2K cakes with largest maximum values. Their sum is a candidate answer.
# However, we must be able to pair the selected cakes. A pair can be formed arbitrarily;
# the only restriction is that the total number of cakes taken from each dimension (where we
# consider the dimension that provides the maximum for that cake) must be even, because each
# pair will use exactly one cake from each of the two cakes and the overall maximum of the
# pair will be at least the sum of the two chosen maximums. If a dimension count is odd, we
# need to adjust by either switching the dimension used for a selected cake or swapping a
# selected cake with an unselected one. The adjustment with the smallest loss yields the
# optimal total.

import sys

def solve_one(N, K, arr):
    # arr: list of triples (X, Y, Z)
    best = []  # (best_val, best_dim, triple)
    for triple in arr:
        x, y, z = triple
        vals = (x, y, z)
        best_val = max(vals)
        best_dim = vals.index(best_val)  # first occurrence if ties
        best.append((best_val, best_dim, vals))

    # order indices by best_val descending
    order = sorted(range(N), key=lambda i: best[i][0], reverse=True)
    selected_set = set(order[:2 * K])
    sum_best = sum(best[i][0] for i in selected_set)

    # count how many selected cakes have each best_dim
    cnt = [0, 0, 0]
    for i in selected_set:
        cnt[best[i][1]] += 1
    odd_dims = [d for d in range(3) if cnt[d] % 2 == 1]
    # If all even, we are done
    if not odd_dims:
        return sum_best

    # There will be exactly two odd dimensions (cannot be three because total selected is even)
    A, B = odd_dims[0], odd_dims[1]
    INF = 10 ** 30

    # Option 1: switch dimension of a selected cake (keep same cake set)
    min_switch_loss = INF
    for i in selected_set:
        val, dim, vals = best[i]
        if dim == A:
            # switch to B, lose (val - vals[B])
            loss = val - vals[B]
            if loss < min_switch_loss:
                min_switch_loss = loss
        elif dim == B:
            loss = val - vals[A]
            if loss < min_switch_loss:
                min_switch_loss = loss
    # Option 2: replace one selected cake of one odd dimension with an unselected cake of the other odd dimension
    # Find minimal best_val among selected of each odd dimension
    min_sel_A = INF
    min_sel_B = INF
    for i in selected_set:
        val, dim, _ = best[i]
        if dim == A and val < min_sel_A:
            min_sel_A = val
        if dim == B and val < min_sel_B:
            min_sel_B = val
    # Find maximal best_val among unselected of each odd dimension
    max_uns_A = -1
    max_uns_B = -1
    for i in order[2 * K:]:  # remaining items are sorted descending, so first occurrence gives max
        val, dim, _ = best[i]
        if dim == A and val > max_uns_A:
            max_uns_A = val
        if dim == B and val > max_uns_B:
            max_uns_B = val
        # early stop if both found max possible (since sorted) ? not needed
    min_replace_loss = INF
    if max_uns_B != -1 and min_sel_A != INF:
        # replace a selected A with an unselected B
        loss = min_sel_A - max_uns_B
        if loss < min_replace_loss:
            min_replace_loss = loss
    if max_uns_A != -1 and min_sel_B != INF:
        loss = min_sel_B - max_uns_A
        if loss < min_replace_loss:
            min_replace_loss = loss

    best_loss = min(min_switch_loss, min_replace_loss)
    return sum_best - best_loss


def solve():
    input_data = sys.stdin.read().strip().split()
    it = iter(input_data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        N = int(next(it))
        K = int(next(it))
        arr = []
        for _ in range(N):
            x = int(next(it)); y = int(next(it)); z = int(next(it))
            arr.append((x, y, z))
        out_lines.append(str(solve_one(N, K, arr)))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
