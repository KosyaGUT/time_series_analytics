# ---------------------------------------------
# Практическая работа №2
# Корреляционный анализ случайных данных
# ---------------------------------------------

import csv
import math

data = {
    "aimp": [...],
    "amud": [...],
    "arnd": [...],
    "asin1": [...],
    "bfo2": [...],
    "bso1": [...],
    "cfo1": [...]
}

# ---------------------------------------------
# 1. Чтение данных
# ---------------------------------------------

LIMIT = 100_000  # первые 100К строк
columns_to_read = ["aimp", "amud", "arnd", "asin1", "bfo2", "bso1", "cfo1"]

data = {col: [] for col in columns_to_read}  # создаём пустые списки для каждого столбца

with open("data.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)

    # Находим индексы нужных столбцов
    indices = {}
    for col in columns_to_read:
        try:
            indices[col] = header.index(col)
        except ValueError:
            print(f"Столбец '{col}' не найден в заголовках")
            continue

    # Читаем строки
    for i, row in enumerate(reader):
        if i >= LIMIT:
            break
        for col, idx in indices.items():
            try:
                data[col].append(float(row[idx]))
            except (ValueError, IndexError):
                # Если значение не число или индекс вне диапазона
                data[col].append(None)  # или пропустить, но лучше сохранить пропуск

# ---------------------------------------------
# 2. Среднее и стандартное отклонение
# ---------------------------------------------

def sum_list(values):
    total = 0.0
    for valueSum in values:
        total += valueSum
    return total

means = {}

stds = {}

for key, value in data.items():
    mean = sum_list(value) / len(value)
    std = math.sqrt(sum_list([(x - mean) ** 2 for x in value])/len(value))
    means[key] = mean
    stds[key] = std
    print(f'Значение: {key} --------------------------\n'
          f'Среднее отклонение: {mean};\n'
          f'Стандартное отклонение: {std}\n')

# ---------------------------------------------
# 3. Корреляция Пирсона
# ---------------------------------------------

def corPirse(x, mean_x, std_x, y, mean_y, std_y):
    total = 0
    for j in range(len(x)):
        total += (x[j] - mean_x) * (y[j] - mean_y)
    return total / (len(x) * std_y * std_x)

matrix_cor = {col: [] for col in columns_to_read}
for key_X, value_X in data.items():
    print(f'{key_X:>10}', end='')
    for key_Y, value_Y in data.items():
        r = corPirse(value_X, means[key_X], stds[key_X], value_Y, means[key_Y], stds[key_Y])
        matrix_cor[key_Y].append(r)
print()
for key_matrix, values_matrix in matrix_cor.items():
    print(f'{key_matrix:<6}', end='')
    for value_matrix in values_matrix:
        print(f'{value_matrix:<10.3f}', end='')
    print()

# ---------------------------------------------
# 4. Проверка значимости (t-критерий)
# ---------------------------------------------

def znachimost(key, values):
    t_dict = {}
    for k, r_value in enumerate(values):
        if r_value >= 1:
            # (корреляция признака с самим собой) действительно не нуждаются в проверке значимости, а
            # погрешности, приводящие к значениям чуть больше 1, будут отфильтрованы.
            continue
        t_znach = r_value * math.sqrt((100_000 - 2) / (1 - r_value ** 2))
        t_dict[f"{key} & {columns_to_read[k]}"] = t_znach
    return t_dict
t_criteria = {}
for key_matrix, values_matrix in matrix_cor.items():
    t = znachimost(key_matrix, values_matrix)
    for k, v in t.items():
        if k not in t_criteria:
            t_criteria[k] = v

print()
for key, values in t_criteria.items():
    print(f"У пары {key:^13} следующий t-критерий = {values:.4f}")

# ---------------------------------------------
# 5. Корреляция Спирмена
# ---------------------------------------------

def get_ranks(arr):
    n = len(arr)

    # (значение, индекс)
    indexed = [(value, i) for i, value in enumerate(arr)]
    indexed.sort(key=lambda x: x[0])

    ranks = [0] * n

    i = 0
    while i < n:
        j = i

        # ищем одинаковые значения
        while j < n and indexed[j][0] == indexed[i][0]:
            j += 1

        # средний ранг
        avg_rank = (i + j - 1) / 2 + 1

        for k in range(i, j):
            ranks[indexed[k][1]] = avg_rank

        i = j

    return ranks


def mean_std(arr):
    n = len(arr)
    mean = sum(arr) / n
    var = sum((x - mean) ** 2 for x in arr) / n
    return mean, var ** 0.5


def corPirseRank(x, y):
    n = len(x)

    mean_x, std_x = mean_std(x)
    mean_y, std_y = mean_std(y)

    total = 0
    for i in range(n):
        total += (x[i] - mean_x) * (y[i] - mean_y)

    return total / (n * std_x * std_y)


# --- 1. Считаем ранги ОДИН раз ---
ranks_data = {}
for key, values in data.items():
    ranks_data[key] = get_ranks(values)


# --- 2. Считаем матрицу Спирмена ---
matrix_cor_rank = {col: [] for col in columns_to_read}

for key_X in columns_to_read:
    print(f'{key_X:>10}', end='')

    for key_Y in columns_to_read:
        r = corPirseRank(
            ranks_data[key_X],
            ranks_data[key_Y]
        )
        matrix_cor_rank[key_Y].append(r)

print()

for key_matrix, values_matrix in matrix_cor_rank.items():
    print(f'{key_matrix:<6}', end='')
    for value_matrix in values_matrix:
        print(f'{value_matrix:<10.3f}', end='')
    print()

# ---------------------------------------------
# 6. Сравнение Пирсон vs Спирмен
# ---------------------------------------------

for name in columns_to_read:
    for digit in range(7):
        pirs = matrix_cor[name][digit]
        spir = matrix_cor_rank[name][digit]
        bool_res = False
        if math.fabs(pirs - spir) < 0.5:
            bool_res = True
        print(f"Корреляция Пирсона ({pirs:.4f}) и корреляция Спирмена ({spir:.4f}) имеют {'линейную связь' if bool_res else 'нелинейную связь'} (Разность: {pirs-spir:.4f})")