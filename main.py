# 1. Чтение CSV в Python
import csv
import math

values = []

# 2. Простой способ прочитать CSV
with open("data.csv", "r") as file:
    reader = csv.reader(file)

    first_row = next(reader)

    # 3. Найдём номер столбца bfo2
    bfo2_index = first_row.index("bfo2")

    # 4. Читаем только колонку bfo2
    for row in reader:
        value = float(row[bfo2_index])
        values.append(value)

    # 5. Теперь найдём минимум и максимум
    min_value = values[0]
    max_value = values[0]

    # Это алгоритм поиска минимума и максимума.
    for v in values:
        if v < min_value:
            min_value = v

        if v > max_value:
            max_value = v

    print("MIN =", min_value)
    print("MAX =", max_value)
# ------------------------------------------------------------------------------
    # 1. Объём выборки
    n = len(values)

    print("Объем выборки n =", n)

    # 2. Число интервалов (формула Стерджесса)
    # Формула: m = 1 + log2(n)

    m = 1 + math.log2(n)
    m = int(round(m))

    print("Количество интервалов m =", m)

    # 3. Ширина интервала
    x_min = min_value
    x_max = max_value

    delta = (x_max - x_min) / m

    print("Ширина интервала Δx =", delta)

    # 4. Построение границ интервалов [x0,x1),[x1,x2),...,[xm−1,xm]
    intervals = []

    left = x_min

    for i in range(m):
        right = left + delta
        intervals.append((left, right))
        left = right

    print("Интервалы:")
    for interval in intervals:
        print(interval)


    # 5. Частоты (сколько значений попало в интервал)
    frequencies = [0] * m

    for value in values:

        if value == x_max:
            frequencies[m - 1] += 1

        for i in range(m):

            left, right = intervals[i]

            if left <= value < right:
                frequencies[i] += 1
                break

    # 6. Вывод статистического ряда
    print("\nСтатистический ряд\n")

    for i in range(m):
        left, right = intervals[i]
        print(f"[{left:.2f}; {right:.2f}] -> {frequencies[i]}")