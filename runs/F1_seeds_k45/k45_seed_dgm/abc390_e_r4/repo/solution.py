def solve():
    N, X = map(int, input().split())
    
    foods = []
    for _ in range(N):
        V, A, C = map(int, input().split())
        foods.append((V - 1, A, C))  # Convert vitamin to 0-indexed
    
    # DP: state = (v1, v2, v3) -> minimum calories needed to achieve this state
    all_states = {}
    all_states[(0, 0, 0)] = 0
    
    for v_idx, amount, calories in foods:
        new_states = {}
        
        for (v1, v2, v3), cal in all_states.items():
            # Option 1: Don't take this food
            key = (v1, v2, v3)
            if key not in new_states:
                new_states[key] = cal
            else:
                new_states[key] = min(new_states[key], cal)
            
            # Option 2: Take this food if we have enough calories
            if cal + calories <= X:
                new_v = [v1, v2, v3]
                new_v[v_idx] += amount
                key = tuple(new_v)
                if key not in new_states:
                    new_states[key] = cal + calories
                else:
                    new_states[key] = min(new_states[key], cal + calories)
        
        all_states = new_states
        
        # Prune states to control memory usage
        # Keep states with high min value and lower calorie cost
        if len(all_states) > 100000:
            scored = []
            for state, cal in all_states.items():
                min_val = min(state)
                cal_left = X - cal
                score = (min_val, cal_left)
                scored.append((score, state, cal))
            
            scored.sort(reverse=True)
            all_states = {state: cal for _, state, cal in scored[:50000]}
    
    # Find the maximum min value among all achievable states
    answer = 0
    for (v1, v2, v3), cal in all_states.items():
        answer = max(answer, min(v1, v2, v3))
    
    print(answer)

solve()
