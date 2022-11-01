import random
import time
import tkinter as tk
from tkinter import messagebox
from functools import partial


def player_choice():
    choice = random.randint(0, 1)
    if choice == 0:
        res = 'Первый ход компьютера'
        sign_c = 'X'
        sign_h = 'O'
    else:
        res = 'Первый ход ваш'
        sign_c = 'O'
        sign_h = 'X'
    return res, sign_c, sign_h


def check_empty_points(game_field):
    # выбор всех пустых клеток на поле
    empty = []
    for i in range(10):
        for j in range(10):
            if game_field[i][j] != 'X' and game_field[i][j] != 'O':
                point = i*10 + j
                empty.append(point)
    return empty


def choose_comp_point(empty_points_list):
    # компьютер выбирает случайную точку на поле
    point = random.choice(empty_points_list)
    point_coords = (point // 10, point % 10)
    return point_coords


def add_mark(point, sign, color):
    # добавляем отметку на игровое поле
    x = point[0]
    y = point[1]
    field[x][y] = sign
    buttons[x][y]['text'] = sign
    buttons[x][y]['bg'] = color


def surrounding_points(point_coord):
    # находим координаты точек вокруг введенной точки (против часовой стрелки, начиная с левого верхнего угла)
    point1 = (point_coord[0] - 1, point_coord[1] - 1)
    point2 = (point_coord[0], point_coord[1] - 1)
    point3 = (point_coord[0] + 1, point_coord[1] - 1)
    point4 = (point_coord[0] + 1, point_coord[1])
    point5 = (point_coord[0] + 1, point_coord[1] + 1)
    point6 = (point_coord[0], point_coord[1] + 1)
    point7 = (point_coord[0] - 1, point_coord[1] + 1)
    point8 = (point_coord[0] - 1, point_coord[1])

    points = [point1, point2, point3, point4, point5, point6, point7, point8]
    points_res = [point for point in points if (0 <= point[0] <= 9) and (0 <= point[1] <= 9)]

    return points_res


def filled_points(surr_points):
    # проверяем наличие заполненных полей вокруг введенной точки
    filled_x = {}
    filled_o = {}
    for i, point in enumerate(surr_points):
        x_coord = point[0]
        y_coord = point[1]
        if field[x_coord][y_coord] == 'X':
            filled_x[i] = point
        elif field[x_coord][y_coord] == 'O':
            filled_o[i] = point
    return filled_x, filled_o


def filled_points_qty(init_point, surr_point, sign):
    # проверяем точки в одном ряду с init_point и surr_point
    def counting(ind_1, ind_2):
        nonlocal init_point
        nonlocal sign
        count = 0
        for i in range(1, 5):
            new_point = (init_point[0] + ind_1 * i, init_point[1] + ind_2 * i)
            x = new_point[0]
            y = new_point[1]
            if (0 <= x <= 9) and (0 <= y <= 9):
                if field[x][y] == sign:
                    count += 1
                else:
                    break
        return count

    ind1 = surr_point[0] - init_point[0]
    ind2 = surr_point[1] - init_point[1]
    qty_one_side = counting(ind1, ind2)
    qty_another_side = counting(-ind1, -ind2)
    return qty_one_side + qty_another_side + 1


def find_winner(filled_x, filled_o, init_point, sign):
    win = ''
    filled_dict = {}
    other_sign = ''

    if sign == 'X':
        filled_dict = filled_x
        other_sign = 'O'
    elif sign == 'O':
        filled_dict = filled_o
        other_sign = 'X'

    for key in filled_dict:
        if key in range(4):
            filled_qty = filled_points_qty(init_point, filled_dict[key], sign)
            if filled_qty >= 5:
                win = other_sign
    return win


def start_button():
    global sign_comp
    global sign_hum
    global buttons
    global field

    messagebox.showinfo('Выбор очередности хода', 'Сейчас мы выберем, кто будет ходить первым')
    choice, sign_comp, sign_hum = player_choice()
    time.sleep(0.2)
    messagebox.showinfo('Выбор очередности хода', f'{choice}')

    for i in range(10):
        for j in range(10):
            buttons[i][j]['state'] = 'normal'

    if sign_comp == 'X':
        empty_points = check_empty_points(field)
        comp_point = choose_comp_point(empty_points)
        add_mark(comp_point, sign_comp, color='dark green')


def field_button_coords(i, j):
    # ход пользователя
    empty_points = check_empty_points(field)
    if (i*10 + j) in empty_points:
        hum_point = (i, j)
        add_mark(hum_point, sign_hum, color='gold')

        surround = surrounding_points(hum_point)
        filled_x, filled_o = filled_points(surround)
        winner = find_winner(filled_x, filled_o, hum_point, sign_hum)
        if winner:
            messagebox.showinfo(message='Победил компьютер')
            time.sleep(1)
            window.quit()

        time.sleep(0.1)

        # ход компьютера
        empty_points = check_empty_points(field)
        comp_point = choose_comp_point(empty_points)
        add_mark(comp_point, sign_comp, color='dark green')

        surround = surrounding_points(comp_point)
        filled_x, filled_o = filled_points(surround)
        winner = find_winner(filled_x, filled_o, comp_point, sign_comp)
        if winner:
            messagebox.showinfo(message='Вы победили. Поздравляю!')
            time.sleep(1)
            window.quit()
    else:
        print('No way')


# игровое поле
field = [[(j*10 + i) for i in range(10)] for j in range(10)]
sign_comp = ''
sign_hum = ''

window = tk.Tk()
window.title('Tic-tac-toe')
window.geometry('615x650')

frame_start = tk.Frame(master=window, relief=tk.FLAT, borderwidth=4, bg='light sky blue')
frame_field = tk.Frame(master=window, relief=tk.FLAT, borderwidth=3, bg='light sky blue')

# кнопка "Старт"
start_btn = tk.Button(master=frame_start, text='Старт', bg='blue2', fg='white', font=("Arial Bold", 20),
                      width=10, command=start_button)
start_btn.grid(row=0, column=0)

# кнопки на поле
buttons = []
for i in range(10):
    buttons.append([])
    for j in range(10):
        field_button = partial(field_button_coords, i, j)
        btn = tk.Button(master=frame_field, text='', bg='RoyalBlue1', width=7, height=3,
                        state='disabled', command=field_button)
        buttons[i].append(btn)
        btn.grid(row=i, column=j, padx=1, pady=1)

frame_start.pack(fill=tk.X)
frame_field.pack(fill=tk.X)

window.mainloop()
