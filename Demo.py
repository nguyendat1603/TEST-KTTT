import random
import math

# ===== FITNESS FUNCTION =====
def fitness(x):
    return x * math.sin(10 * x) + x * x

# ===== INITIAL POPULATION =====
def init_population(n):
    return [random.uniform(-10, 10) for _ in range(n)]

# ===== SELECTION (Roulette) =====
def selection(pop):
    fits = [fitness(x) for x in pop]
    total = sum(fits)
    r = random.uniform(0, total)
    acc = 0
    for i, f in enumerate(fits):
        acc += f
        if acc >= r:
            return pop[i]
    return pop[-1]

# ===== SBX CROSSOVER =====
def sbx_crossover(p1, p2, eta=20):
    # 90% probability crossover
    if random.random() > 0.9:
        return p1, p2

    u = random.random()
    if u <= 0.5:
        beta = (2 * u)**(1 / (eta + 1))
    else:
        beta = (1 / (2 * (1 - u)))**(1 / (eta + 1))

    c1 = 0.5 * ((1 + beta) * p1 + (1 - beta) * p2)
    c2 = 0.5 * ((1 - beta) * p1 + (1 + beta) * p2)

    # CLAMP VỀ [-10, 10]
    c1 = max(-10, min(10, c1))
    c2 = max(-10, min(10, c2))

    return c1, c2

# ===== POLYNOMIAL MUTATION =====
def polynomial_mutation(x, eta=20, p=0.05):   # Giảm mutation rate
    if random.random() > p:
        return x

    u = random.random()
    if u < 0.5:
        delta = (2 * u)**(1 / (eta + 1)) - 1
    else:
        delta = 1 - (2 * (1 - u))**(1 / (eta + 1))

    x_new = x + delta

    # CLAMP luôn sau mutation
    return max(-10, min(10, x_new))

# ===== GA MAIN LOOP =====
pop = init_population(30)

for gen in range(50):
    new_pop = []

    # ==== ELITISM: lấy cá thể tốt nhất thế hệ cũ ====
    best_old = max(pop, key=fitness)

    # Tạo cá thể mới
    while len(new_pop) < 30:
        p1 = selection(pop)
        p2 = selection(pop)

        c1, c2 = sbx_crossover(p1, p2)
        c1 = polynomial_mutation(c1)
        c2 = polynomial_mutation(c2)

        new_pop.append(c1)
        if len(new_pop) < 30:
            new_pop.append(c2)

    # ==== GÁN LẠI CÁ THỂ TỐT NHẤT ====
    new_pop[0] = best_old

    pop = new_pop

    if gen % 10 == 0:
        best = max(pop, key=fitness)
        print(f"Gen {gen}: best x = {best:.4f}, fitness = {fitness(best):.4f}")

# ===== FINAL RESULT =====
best = max(pop, key=fitness)
print("\n===== KẾT QUẢ CUỐI =====")
print("Best x =", best)
print("Best fitness =", fitness(best))
