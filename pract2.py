# ---------------------------------------------
# Практическая работа №2
# Корреляционный анализ случайных данных
# ---------------------------------------------

import csv
import math

LIMIT = 100_000
columns_to_read = ["aimp", "amud", "arnd", "asin1", "bfo2", "bso1", "cfo1"]

# ---------------------------------------------
# 1. Чтение данных
# ---------------------------------------------

data = {col: [] for col in columns_to_read}

with open("data.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)

    indices = {}
    for col in columns_to_read:
        if col in header:
            indices[col] = header.index(col)
        else:
            print(f"Столбец {col} не найден в файле")

    for i, row in enumerate(reader):
        if i >= LIMIT:
            break

        try:
            values = [float(row[indices[col]]) for col in columns_to_read]
        except (ValueError, IndexError, KeyError):
            continue

        for col, value in zip(columns_to_read, values):
            data[col].append(value)


# ---------------------------------------------
# 2. Среднее и стандартное отклонение
# ---------------------------------------------

def mean_std(values):
    n = len(values)
    mean_value = sum(values) / n
    variance = sum((x - mean_value) ** 2 for x in values) / n
    return mean_value, math.sqrt(variance)


means = {}
stds = {}

print("\n2. Среднее и стандартное отклонение\n")
for name, values in data.items():
    mean_value, std_value = mean_std(values)
    means[name] = mean_value
    stds[name] = std_value

    print(f"{name}:")
    print(f"  Среднее значение      = {mean_value:.6f}")
    print(f"  Стандартное отклонение = {std_value:.6f}\n")


# ---------------------------------------------
# 3. Корреляция Пирсона
# ---------------------------------------------

def pearson_corr(x, mean_x, std_x, y, mean_y, std_y):
    total = 0.0
    n = len(x)

    for i in range(n):
        total += (x[i] - mean_x) * (y[i] - mean_y)

    return total / (n * std_x * std_y)


matrix_pearson = {col: [] for col in columns_to_read}

print("3. Корреляция Пирсона\n")
print(f"{'':>8}", end="")
for col in columns_to_read:
    print(f"{col:>10}", end="")
print()

for key_x in columns_to_read:
    print(f"{key_x:>8}", end="")
    for key_y in columns_to_read:
        r = pearson_corr(
            data[key_x], means[key_x], stds[key_x],
            data[key_y], means[key_y], stds[key_y]
        )
        matrix_pearson[key_y].append(r)
        print(f"{r:>10.3f}", end="")
    print()


# ---------------------------------------------
# 4. Проверка значимости (t-критерий)
# ---------------------------------------------

def t_statistic(r, n):
    if abs(r) >= 1.0:
        return float("inf")
    return abs(r) * math.sqrt((n - 2) / (1 - r ** 2))


n = len(next(iter(data.values())))
t_critical = 1.96  # приближённо для alpha = 0.05 при больших n

print("\n4. Проверка значимости (t-критерий)\n")
for i, key_x in enumerate(columns_to_read):
    for j in range(i + 1, len(columns_to_read)):
        key_y = columns_to_read[j]
        r = matrix_pearson[key_y][i]
        t_value = t_statistic(r, n)
        significance = "значима" if t_value > t_critical else "не значима"
        print(f"{key_x:>6} & {key_y:<6}  r = {r:>8.4f}  t = {t_value:>10.4f}  связь {significance}")


# ---------------------------------------------
# 5. Корреляция Спирмена
# ---------------------------------------------

def get_ranks(values):
    n = len(values)

    indexed = [(value, i) for i, value in enumerate(values)]
    indexed.sort(key=lambda x: x[0])

    ranks = [0.0] * n
    i = 0

    while i < n:
        j = i
        while j < n and indexed[j][0] == indexed[i][0]:
            j += 1

        # средний ранг для одинаковых значений
        avg_rank = (i + j - 1) / 2 + 1

        for k in range(i, j):
            ranks[indexed[k][1]] = avg_rank

        i = j

    return ranks


ranks_data = {}
for name, values in data.items():
    ranks_data[name] = get_ranks(values)


def spearman_corr(x, y):
    mean_x, std_x = mean_std(x)
    mean_y, std_y = mean_std(y)

    total = 0.0
    n = len(x)

    for i in range(n):
        total += (x[i] - mean_x) * (y[i] - mean_y)

    return total / (n * std_x * std_y)


matrix_spearman = {col: [] for col in columns_to_read}

print("\n5. Корреляция Спирмена\n")
print(f"{'':>8}", end="")
for col in columns_to_read:
    print(f"{col:>10}", end="")
print()

for key_x in columns_to_read:
    print(f"{key_x:>8}", end="")
    for key_y in columns_to_read:
        r = spearman_corr(ranks_data[key_x], ranks_data[key_y])
        matrix_spearman[key_y].append(r)
        print(f"{r:>10.3f}", end="")
    print()


# ---------------------------------------------
# 6. Сравнение Пирсон vs Спирмен
# ---------------------------------------------

print("\n6. Сравнение Пирсон vs Спирмен\n")
for i, key_x in enumerate(columns_to_read):
    for j in range(i + 1, len(columns_to_read)):
        key_y = columns_to_read[j]

        pearson_r = matrix_pearson[key_y][i]
        spearman_r = matrix_spearman[key_y][i]
        diff = abs(pearson_r - spearman_r)

        if diff < 0.1:
            relation = "связь близка к линейной"
        elif abs(spearman_r) > abs(pearson_r):
            relation = "есть признаки нелинейной монотонной связи"
        else:
            relation = "связь частично нелинейная или слабее линейной"

        print(
            f"{key_x:>6} & {key_y:<6}  "
            f"Пирсон = {pearson_r:>8.4f}, "
            f"Спирмен = {spearman_r:>8.4f}, "
            f"разность = {diff:>8.4f}  -> {relation}"
        )


# ---------------------------------------------
# 7. Коэффициент Кендалла tau-b
# ---------------------------------------------

def kendall_tau_b(x, y):
    n = len(x)
    concordant = 0
    discordant = 0
    ties_x = 0
    ties_y = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]

            if dx == 0 and dy == 0:
                continue
            elif dx == 0:
                ties_x += 1
            elif dy == 0:
                ties_y += 1
            else:
                prod = dx * dy
                if prod > 0:
                    concordant += 1
                elif prod < 0:
                    discordant += 1

    denom = math.sqrt((concordant + discordant + ties_x) * (concordant + discordant + ties_y))
    if denom == 0:
        return 0.0

    return (concordant - discordant) / denom


print("\n7. Коэффициент Кендалла\n")

kendall_pairs = [
    ("aimp", "bfo2"),
    ("arnd", "bso1"),
]

# Для Кендалла лучше брать меньшую подвыборку,
# иначе алгоритм O(n^2) станет очень медленным
kendall_limit = 3000

for x_name, y_name in kendall_pairs:
    x_values = data[x_name][:kendall_limit]
    y_values = data[y_name][:kendall_limit]

    tau = kendall_tau_b(x_values, y_values)
    print(f"{x_name:>6} & {y_name:<6}  tau = {tau:.4f}")


# ---------------------------------------------
# 8. Интерпретация связи
# ---------------------------------------------

def interpret_relation(x_name, y_name, pearson_r, spearman_r):
    abs_p = abs(pearson_r)
    abs_s = abs(spearman_r)
    diff = abs(pearson_r - spearman_r)

    if abs_p < 0.2:
        strength = "слабая"
    elif abs_p < 0.5:
        strength = "умеренная"
    else:
        strength = "сильная"

    if diff < 0.1:
        nature = "связь в основном линейная или близкая к линейной"
    elif abs_s > abs_p:
        nature = "связь скорее монотонная, но не строго линейная"
    else:
        nature = "связь может быть нелинейной или зависеть от режима работы системы"

    print(f"{x_name:>6} & {y_name:<6} -> {strength} корреляция, {nature}")


print("\n8. Интерпретация\n")
interpret_pairs = [
    ("aimp", "bfo2"),
    ("arnd", "bso1"),
    ("bso1", "cfo1"),
    ("amud", "bso1"),
]

for x_name, y_name in interpret_pairs:
    i = columns_to_read.index(x_name)
    pearson_r = matrix_pearson[y_name][i]
    spearman_r = matrix_spearman[y_name][i]
    interpret_relation(x_name, y_name, pearson_r, spearman_r)