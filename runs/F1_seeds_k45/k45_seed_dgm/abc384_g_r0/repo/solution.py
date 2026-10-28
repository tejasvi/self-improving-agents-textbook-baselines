import sys

def main():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    # Precompute prefix sums for A and B
    prefix_A = [0] * (N + 1)
    prefix_B = [0] * (N + 1)
    
    for i in range(N):
        prefix_A[i + 1] = prefix_A[i] + A[i]
        prefix_B[i + 1] = prefix_B[i] + B[i]
    
    # Process each query
    for _ in range(K):
        x, y = map(int, input().split())
        
        # For each A_i (i = 1..x), we need to compute sum of |A_i - B_j| for j = 1..y
        # This can be expanded as:
        # sum_i sum_j |A_i - B_j|
        # = sum_i sum_j (A_i - B_j) if A_i >= B_j
        # = sum_i sum_j (B_j - A_i) if B_j > A_i
        
        # A more efficient approach:
        # For each A_i, count how many B_j are less than A_i and how many are greater
        # But even better: use the fact that:
        # sum |A_i - B_j| = sum A_i * count(B_j <= some value) - sum B_j * count(A_i <= some value) + adjustments
        
        # Actually, let's compute it directly but efficiently:
        # sum_i=1^x sum_j=1^y |A_i - B_j|
        # We can iterate through each A_i and for each, compute the sum with B_1..B_y
        
        result = 0
        
        # For each element in A (up to index x)
        for i in range(x):
            # Sum |A[i] - B[j]| for j in range(y)
            for j in range(y):
                result += abs(A[i] - B[j])
        
        print(result)

if __name__ == "__main__":
    main()
