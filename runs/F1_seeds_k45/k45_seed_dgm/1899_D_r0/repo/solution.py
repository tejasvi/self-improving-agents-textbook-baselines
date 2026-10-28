def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                # Check if a_i * 2^{a_j} == a_j * 2^{a_i}
                # This can overflow for large exponents, so we need careful handling
                
                # If a_i == a_j, they always satisfy the condition
                if a[i] == a[j]:
                    count += 1
                else:
                    # We need to check: a_i * 2^{a_j} == a_j * 2^{a_i}
                    # For safety, let's compute with Python's arbitrary precision
                    ai, aj = a[i], a[j]
                    
                    lhs = ai * (2 ** aj)
                    rhs = aj * (2 ** ai)
                    
                    if lhs == rhs:
                        count += 1
        
        print(count)

solve()
