# ---------------------------------------------
# Лабораторная работа по статистическому анализу
# Анализ распределения случайной величины
# ---------------------------------------------

import csv
import math

values = []

# ---------------------------------------------
# 1. Чтение CSV файла
# ---------------------------------------------

with open("data.csv", "r") as file:

    reader = csv.reader(file)

    header = next(reader)

    # Находим индекс столбца bfo2
    bfo2_index = header.index("bfo2")

    # Считываем значения столбца
    for row in reader:
        value = float(row[bfo2_index])
        values.append(value)

# ---------------------------------------------
# 2. Поиск минимума и максимума
# ---------------------------------------------

min_value = values[0]
max_value = values[0]

for v in values:

    if v < min_value:
        min_value = v

    if v > max_value:
        max_value = v

print("MIN =", min_value)
print("MAX =", max_value)

# ---------------------------------------------
# 3. Объем выборки
# ---------------------------------------------

n = len(values)

print("Объем выборки n =", n)

# ---------------------------------------------
# 4. Число интервалов (формула Стерджесса)
# m = 1 + log2(n)
# ---------------------------------------------

m = int(1 + math.log2(n))

print("Количество интервалов m =", m)

# ---------------------------------------------
# 5. Ширина интервала
# Δx = (xmax - xmin) / m
# ---------------------------------------------

x_min = min_value
x_max = max_value

delta = (x_max - x_min) / m

print("Ширина интервала Δx =", delta)

# ---------------------------------------------
# 6. Построение интервалов
# ---------------------------------------------

intervals = []

left = x_min

for i in range(m):

    right = left + delta
    intervals.append((left, right))
    left = right

print("Интервалы:")

for interval in intervals:
    print(interval)

# ---------------------------------------------
# 7. Подсчет частот
# ---------------------------------------------

frequencies = [0] * m

for value in values:

    if value == x_max:
        frequencies[m - 1] += 1
        continue

    for i in range(m):

        left, right = intervals[i]

        if left <= value < right:
            frequencies[i] += 1
            break

# ---------------------------------------------
# 8. Вывод статистического ряда
# ---------------------------------------------

print("\nСтатистический ряд\n")

for i in range(m):

    left, right = intervals[i]

    print(f"[{left:.2f}; {right:.2f}] -> {frequencies[i]}")

# ---------------------------------------------
# 9. Относительные частоты
# pi = ni / n
# ---------------------------------------------

relative_freq = []

for freq in frequencies:
    p = freq / n
    relative_freq.append(p)

# ---------------------------------------------
# 10. Накопленные частоты
# ---------------------------------------------

cumulative_freq = []

current_sum = 0

for freq in frequencies:
    current_sum += freq
    cumulative_freq.append(current_sum)

# ---------------------------------------------
# 11. Вывод интервального статистического ряда
# ---------------------------------------------

print("\nИнтервальный статистический ряд:\n")

for i in range(m):

    left, right = intervals[i]
    freq = frequencies[i]
    rel = relative_freq[i]
    cum = cumulative_freq[i]

    print(f"[{left:.2f}; {right:.2f}]  n={freq}  p={rel:.6f}  F={cum}")

# ---------------------------------------------
# 12. Выборочное среднее
# ---------------------------------------------

sum_x = 0

for v in values:
    sum_x += v

mean = sum_x / n

print("\nСреднее значение =", mean)

# ---------------------------------------------
# 13. Дисперсия
# ---------------------------------------------

sum_sq = 0

for v in values:

    diff = v - mean
    sum_sq += diff * diff

variance = sum_sq / n

print("Дисперсия =", variance)

# ---------------------------------------------
# 14. Стандартное отклонение
# ---------------------------------------------

std_dev = math.sqrt(variance)

print("Стандартное отклонение =", std_dev)

# ---------------------------------------------
# 15. Оценка параметров нормального распределения
# методом моментов
# μ = x̄
# σ = sqrt(D)
# ---------------------------------------------

mu = mean
sigma = std_dev

# ---------------------------------------------
# 16. Функция распределения нормального закона
# ---------------------------------------------

def normal_cdf(x, mu, sigma):

    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

# ---------------------------------------------
# 17. Теоретические вероятности попадания
# в интервалы
# ---------------------------------------------

theoretical_p = []

for left, right in intervals:

    p = normal_cdf(right, mu, sigma) - normal_cdf(left, mu, sigma)

    theoretical_p.append(p)

# ---------------------------------------------
# 18. Ожидаемые частоты
# np_i
# ---------------------------------------------

expected = []

for p in theoretical_p:

    expected.append(n * p)

print("\nТеоретические вероятности и ожидаемые частоты:\n")

for i in range(m):

    left, right = intervals[i]

    print(
        f"[{left:.2f}; {right:.2f}] "
        f"p={theoretical_p[i]:.9f} "
        f"np={expected[i]:.2f}"
    )

# ---------------------------------------------
# 19. Критерий согласия Пирсона
# ---------------------------------------------

chi_square = 0

for i in range(m):

    observed = frequencies[i]
    exp = expected[i]

    if exp > 0:
        chi_square += ((observed - exp) ** 2) / exp

print("\nКритерий Пирсона χ² =", chi_square)

# ---------------------------------------------
# 20. Число степеней свободы
# k = m - s - 1
# где s = число параметров распределения
# для нормального распределения s = 2
# ---------------------------------------------

k = m - 2 - 1

print("Степени свободы =", k)

print("\nДальше χ² сравнивается с табличным значением.")