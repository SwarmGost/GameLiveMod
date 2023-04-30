# Импорты

# import time

import pygame as p
from pygame.locals import *
import random

# Ввод данных о размере поля
q = int(input("Вариант: "))

# Константы
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# COLOR = (255, 0, 0)
pixel = 10                 # Размер отдельного квадратика
sleepTime = 50             # Количество пропускаемых циклов для самедления обсчета
sl = sleepTime             # Установка счетсика циклов на максимум
pause = True               # Пауза - True, обсчет - False
con = 0                    # Общий счетчик циклов (Печатается при остановке)
polex = 700                # Размер в пикселях окна по X
poley = 500                # Размер в пикселях окна по Y
lifeZ = 0.01                # Вероятность зарождения жизни
lifeD = 0.01                # Веростяноть смерти в комфортных условиях
lifeNum = 2                # Количество жизней при зарождении в варианте 3


# Создаем окно
root = p.display.set_mode((polex, poley))
# 2х мерный список с помощью генераторных выражений
# cells = [[random.choice([False, True]) for j in range(root.get_width() // pixel)] for i in range(root.get_height() // pixel)]
# Обнуляем основной массив
cells = [[0 for i in range(poley // pixel)] for j in range(polex // pixel)]

# Функция определения кол-ва соседей
def near(pos: list, system=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]):
    count = 0
    for i in system:
        if cells[(pos[0] + i[0]) % len(cells)][(pos[1] + i[1]) % len(cells[0])] > 0:
            count += 1
    return count

# Основной цикл
while 1:
    # Заполняем экран белым цветом
    root.fill(WHITE)

    # Рисуем сетку
#    for i in range(0, root.get_height() // 1):
#        p.draw.line(root, BLACK, (0, i * pixel), (root.get_width(), i * pixel))
#    for j in range(0, root.get_width() // 1):
#        p.draw.line(root, BLACK, (j * pixel, 0), (j * pixel, root.get_height()))

    # Проходимся по всем клеткам
    for i in range(0, len(cells)):
        for j in range(0, len(cells[i])):
            # Рисуем клетки
            p.draw.rect(root, BLACK if cells[i][j] > 0 else WHITE, [i * pixel, j * pixel, pixel-1, pixel-1])
    # Обновляем экран
    p.display.update()
    # Если не стоим на паузе и не пропускаем циклы, то считаем следующий шаг
    if not pause and sl <= 0:
        cells2 = [[0 for j in range(len(cells[0]))] for i in range(len(cells))]
        for i in range(len(cells)):
            for j in range(len(cells[0])):
                if q == 0:
                    if cells[i][j] > 0:
                        if near([i, j]) not in (2, 3):
                            cells2[i][j] = 0
                            continue
                        cells2[i][j] = 1
                        continue
                    if near([i, j]) == 3:
                        cells2[i][j] = 1
                        continue
                    cells2[i][j] = 0
                elif q == 1:
                    if cells[i][j] > 0:
                        if near([i, j]) not in (2, 3):
                            cells2[i][j] = 0
                            continue
                        if random.random() > lifeD:
                            cells2[i][j] = 1
                        else:
                            cells2[i][j] = 0
                        continue
                    if near([i, j]) == 3:
                        cells2[i][j] = 1
                        continue
                    if random.random() < lifeZ:
                        cells2[i][j] = 1
                    else:
                        cells2[i][j] = 0
                elif q == 2:
                    if cells[i][j] > 0:
                        if near([i, j]) not in (2, 3):
                            cells2[i][j] = cells[i][j] - 1
                            continue
                        cells2[i][j] = cells[i][j] + 1
                        continue
                    if near([i, j]) == 3:
                        cells2[i][j] = cells[i][j] + 1
                        continue
                    cells2[i][j] = 0
                elif q == 3:
                    if cells[i][j] > 0:
                        if near([i, j]) not in (2, 3):
                            cells2[i][j] = cells[i][j] - 1
                            continue
                        cells2[i][j] = cells[i][j]
                        continue
                    if near([i, j]) == 3:
                        cells2[i][j] = lifeNum
                        continue
                    #cells2[i][j] = 0
        cells = cells2
        sl = sleepTime
        con += 1
    else:
        sl -= 1
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit(0)

        if event.type == p.KEYDOWN:
            keys = p.key.get_pressed()
            if keys[p.K_SPACE]:
                pause = not pause
                print(con)
        if event.type == p.MOUSEBUTTONDOWN:
            m = p.mouse.get_pos()
            cells[m[0] // pixel][m[1] // pixel] = not cells[m[0] // pixel][m[1] // pixel]
        continue