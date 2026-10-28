from collections import defaultdict
from itertools import product

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L - 1, R - 1))  # Convert to 0-indexed
    
    def get_covered_positions(ops_list):
        covered = set()
        for i, op in enumerate(ops_list):
            L, R = operations[i]
            if op == 1:
                for j in range(L, R + 1):
                    covered.add(j)
            elif op == 2:
                for j in range(N):
                    if j < L or j > R:
                        covered.add(j)
        return covered
    
    # For small M, use brute force to find optimal solution
    if M <= 20:
        min_cost = float('inf')
        best_ops = None
        
        for ops_combo in product([0, 1, 2], repeat=M):
            covered = get_covered_positions(ops_combo)
            if len(covered) == N:
                cost = sum(1 for op in ops_combo if op != 0)
                if cost < min_cost:
                    min_cost = cost
                    best_ops = ops_combo
        
        if best_ops is None:
            print(-1)
        else:
            print(min_cost)
            print(' '.join(map(str, best_ops)))
    else:
        # For large M, use a greedy set cover approach
        # This might not give optimal solution, but it's better than nothing
        
        ops_result = [0] * M
        covered = set()
        cost = 0
        
        # Track which operations have been used
        used = [False] * M
        
        while len(covered) < N:
            best_op_idx = -1
            best_gain = 0
            best_op_type = 0
            
            uncovered = set(range(N)) - covered
            
            for i in range(M):
                if used[i]:
                    continue
                
                L, R = operations[i]
                
                # Check operation 1
                gain1 = len([j for j in range(L, R + 1) if j in uncovered])
                if gain1 > best_gain:
                    best_gain = gain1
                    best_op_idx = i
                    best_op_type = 1
                
                # Check operation 2
                gain2 = len([j for j in range(N) if (j < L or j > R) and j in uncovered])
                if gain2 > best_gain:
                    best_gain = gain2
                    best_op_idx = i
                    best_op_type = 2
            
            if best_op_idx == -1:
                print(-1)
                return
            
            ops_result[best_op_idx] = best_op_type
            used[best_op_idx] = True
            cost += 1
            
            L, R = operations[best_op_idx]
            if best_op_type == 1:
                for j in range(L, R + 1):
                    covered.add(j)
            else:  # best_op_type == 2
                for j in range(N):
                    if j < L or j > R:
                        covered.add(j)
        
        print(cost)
        print(' '.join(map(str, ops_result)))

solve()
