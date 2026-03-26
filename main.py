# ---------------------------------------------
# Лабораторная работа №1
# Анализ распределения и критерий Пирсона
# ---------------------------------------------

import csv
import math
import matplotlib.pyplot as plt

values = []

# ---------------------------------------------
# 1. Чтение данных (ТОЛЬКО нормальная часть)
# ---------------------------------------------

LIMIT = 1_000_000  # первые 1 млн — без аномалий

with open("data.csv", "r") as file:

    reader = csv.reader(file)
    header = next(reader)

    index = header.index("bfo2")

    for i, row in enumerate(reader):
        if i >= LIMIT:
            break

        values.append(float(row[index]))

# ---------------------------------------------
# 2. Основные параметры
# ---------------------------------------------

n = len(values)
x_min = min(values)
x_max = max(values)

print("n =", n)
print("min =", x_min)
print("max =", x_max)

# ---------------------------------------------
# 3. Число интервалов (Стерджесс)
# ---------------------------------------------

m = int(1 + math.log2(n))
print("m =", m)

delta = (x_max - x_min) / m
print(f"Δ = {delta}\n")
# ---------------------------------------------
# 4. Интервалы
# ---------------------------------------------

intervals = []

left = x_min
for _ in range(m):
    right = left + delta
    intervals.append((left, right))
    left = right

# ---------------------------------------------
# 5. Частоты
# ---------------------------------------------

frequencies = [0] * m

for v in values:

    if v == x_max:
        frequencies[-1] += 1
        continue

    for i in range(m):
        l, r = intervals[i]
        if l <= v < r:
            frequencies[i] += 1
            break

# ---------------------------------------------
# 6. Относительные частоты и плотности
# ---------------------------------------------

relative = [f / n for f in frequencies]
density = [relative[i] / delta for i in range(m)]
midpoints = [(l + r) / 2 for l, r in intervals]

# ---------------------------------------------
# 7. Гистограмма + нормальная кривая
# ---------------------------------------------

plt.figure(figsize=(10, 5))

plt.bar(midpoints, density, width=delta, edgecolor="black", alpha=0.6)

# ---------------------------------------------
# 8. Среднее и σ
# ---------------------------------------------

mean = sum(values) / n
variance = sum((x - mean) ** 2 for x in values) / n
sigma = math.sqrt(variance)

print("\nmean =", mean)
print("sigma =", sigma)

# нормальная плотность
def normal_pdf(x, mu, sigma):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

# рисуем кривую
x_vals = []
y_vals = []

steps = 200
step = (x_max - x_min) / steps

x = x_min
for _ in range(steps):
    x_vals.append(x)
    y_vals.append(normal_pdf(x, mean, sigma))
    x += step

plt.plot(x_vals, y_vals)

plt.title("Гистограмма и нормальное распределение")
plt.xlabel("x")
plt.ylabel("Плотность")
plt.grid()

plt.show()

# ---------------------------------------------
# 9. Функция распределения
# ---------------------------------------------

def normal_cdf(x, mu, sigma):
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

# ---------------------------------------------
# 10. Теоретические вероятности
# ---------------------------------------------

p_theoretical = [
    normal_cdf(r, mean, sigma) - normal_cdf(l, mean, sigma)
    for l, r in intervals
]

expected = [n * p for p in p_theoretical]

# ---------------------------------------------
# 11. Проверка np >= 5
# ---------------------------------------------

print("\nПроверка условия np >= 5:")

for i, exp in enumerate(expected):
    if exp < 5:
        print(f"Интервал {intervals[i]}: np = {exp:.2f} < 5 (нарушение)")

# ---------------------------------------------
# 12. Критерий Пирсона
# ---------------------------------------------

chi2 = 0

for obs, exp in zip(frequencies, expected):
    if exp > 0:
        chi2 += (obs - exp) ** 2 / exp

# степени свободы
k = m - 1 - 2  # 2 параметра (mu, sigma)

print("\nχ² =", chi2)
print("Степени свободы =", k)

# ---------------------------------------------
# 13. Проверка гипотезы
# ---------------------------------------------

alpha = 0.05

# табличное значение можно взять из таблицы (примерно)
# для k ~ 20 → ~31.4 (пример, уточнить по таблице)
chi2_critical = 31.4

print("χ² критическое =", chi2_critical)

if chi2 < chi2_critical:
    print("\nГипотеза H0 принимается (распределение нормальное)")
else:
    print("\nГипотеза H0 отвергается (распределение не нормальное)")