# ---------------------------------------------
# Практическая работа №3
# Нелинейная регрессия (лог-модель)
# ---------------------------------------------

import csv
import math

# ---------------------------------------------
# 1. Чтение данных (ТОЛЬКО нормальная часть)
# ---------------------------------------------

LIMIT = 1_000_000

columns = ["bfo2", "asin1", "arnd", "amud"]
data = {col: [] for col in columns}

with open("data.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)

    indices = {col: header.index(col) for col in columns}

    for i, row in enumerate(reader):
        if i >= LIMIT:
            break

        try:
            bfo2 = float(row[indices["bfo2"]])
            asin1 = float(row[indices["asin1"]])
            arnd = float(row[indices["arnd"]])
            amud = float(row[indices["amud"]])

            # фильтр для логарифма
            if bfo2 > 0 and asin1 > 0 and arnd > 0 and amud >= 0:

                data["bfo2"].append(math.log(bfo2))
                data["asin1"].append(math.log(asin1))
                data["arnd"].append(math.log(arnd))
                data["amud"].append(math.log(amud + 1))

        except:
            continue

n = len(data["bfo2"])

print("\n====================================")
print("ПОДГОТОВКА ДАННЫХ")
print("====================================")
print(f"Количество наблюдений: {n}")

# ---------------------------------------------
# 2. Вспомогательные функции
# ---------------------------------------------

def mean(arr):
    return sum(arr) / len(arr)

def sum_prod(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))

# ---------------------------------------------
# 3. Подготовка переменных
# ---------------------------------------------

Z = data["bfo2"]
X1 = data["asin1"]
X2 = data["arnd"]
X3 = data["amud"]

# суммы
Sx1 = sum(X1)
Sx2 = sum(X2)
Sx3 = sum(X3)
Sz  = sum(Z)

Sx1x1 = sum_prod(X1, X1)
Sx2x2 = sum_prod(X2, X2)
Sx3x3 = sum_prod(X3, X3)

Sx1x2 = sum_prod(X1, X2)
Sx1x3 = sum_prod(X1, X3)
Sx2x3 = sum_prod(X2, X3)

Sx1z = sum_prod(X1, Z)
Sx2z = sum_prod(X2, Z)
Sx3z = sum_prod(X3, Z)

# ---------------------------------------------
# 4. Решение системы (метод Гаусса)
# ---------------------------------------------

A = [
    [n,     Sx1,   Sx2,   Sx3],
    [Sx1,   Sx1x1, Sx1x2, Sx1x3],
    [Sx2,   Sx1x2, Sx2x2, Sx2x3],
    [Sx3,   Sx1x3, Sx2x3, Sx3x3]
]

B = [Sz, Sx1z, Sx2z, Sx3z]

def gauss(A, B):
    n = len(B)

    for i in range(n):
        pivot = A[i][i]

        for j in range(i, n):
            A[i][j] /= pivot
        B[i] /= pivot

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                B[k] -= factor * B[i]

    return B

a, b1, b2, b3 = gauss(A, B)

# ---------------------------------------------
# 5. Вывод модели
# ---------------------------------------------

print("\n====================================")
print("МОДЕЛЬ РЕГРЕССИИ")
print("====================================")

print("ln(Y) = a + b1*ln(asin1) + b2*ln(arnd) + b3*ln(amud)")

print("\nКоэффициенты:")
print(f"a  = {a:.6f}")
print(f"b1 = {b1:.6f} (asin1)")
print(f"b2 = {b2:.6f} (arnd)")
print(f"b3 = {b3:.6f} (amud)")

# ---------------------------------------------
# 6. Интерпретация коэффициентов
# ---------------------------------------------

print("\n====================================")
print("ИНТЕРПРЕТАЦИЯ")
print("====================================")

print(f"asin1 ↑ на 1% -> bfo2 изменится на {b1:.4f}%")
print(f"arnd  ↑ на 1% -> bfo2 изменится на {b2:.4f}%")
print(f"amud  ↑ на 1% -> bfo2 изменится на {b3:.4f}%")

# ---------------------------------------------
# 7. Предсказание
# ---------------------------------------------

Z_pred = []
for i in range(n):
    z = a + b1*X1[i] + b2*X2[i] + b3*X3[i]
    Z_pred.append(z)

# ---------------------------------------------
# 8. Качество модели
# ---------------------------------------------

mean_z = mean(Z)

SS_tot = sum((z - mean_z)**2 for z in Z)
SS_res = sum((Z[i] - Z_pred[i])**2 for i in range(n))

R2 = 1 - SS_res / SS_tot

print("\n====================================")
print("КАЧЕСТВО МОДЕЛИ")
print("====================================")

print(f"R^2 = {R2:.4f}")

if R2 > 0.7:
    print("Модель хорошо объясняет данные")
elif R2 > 0.3:
    print("Модель объясняет данные частично")
else:
    print("Модель слабо объясняет данные")

# ---------------------------------------------
# 9. Ошибка
# ---------------------------------------------

error = sum(abs(Z[i] - Z_pred[i]) for i in range(n)) / n

print("\n====================================")
print("ОШИБКА")
print("====================================")

print(f"Средняя ошибка = {error:.6f}")

if error < 0.1:
    print("Высокая точность")
elif error < 0.3:
    print("Средняя точность")
else:
    print("Низкая точность")

# ---------------------------------------------
# 10. F-критерий
# ---------------------------------------------

k = 3

F = (R2 / k) / ((1 - R2) / (n - k - 1))

print("\n====================================")
print("F-КРИТЕРИЙ")
print("====================================")

print(f"F = {F:.2f}")
print("Если F >> 1 → модель значима")

if F > 10:
    print("Модель статистически значима")
else:
    print("Модель НЕ значима")

# ---------------------------------------------
# 11. Прогноз
# ---------------------------------------------

x1 = X1[-1]
x2 = X2[-1]
x3 = X3[-1]

z_pred = a + b1*x1 + b2*x2 + b3*x3
y_pred = math.exp(z_pred)

print("\n====================================")
print("ПРОГНОЗ")
print("====================================")

print(f"Прогноз Y = {y_pred:.4f}")