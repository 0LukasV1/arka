import tkinter as tk
from random import randrange
import random

def starter(e):
    global x, y
    zoz = canvas.find_overlapping(e.x, e.y, e.x + 1, e.y + 1)
    if desk in zoz:
        x = e.x
        y = e.y
        pohyb()
        canvas.delete(start_text)

def pohyb():
    global lopta, movement, desk
    canvas.move(lopta, movement[0], movement[1])
    pos = canvas.coords(lopta)
    desk_pos = canvas.coords(desk)
    overlap = canvas.find_overlapping(desk_pos[0], desk_pos[1], desk_pos[2], desk_pos[3])
    destroy_brick()
    if pos[2] >= width:
        movement = [movement[0] * -1, movement[1]]
    elif pos[3] >= height:
        canvas.delete('all')
        text = canvas.create_text(width // 2, height // 2, text='Koniec', fill="red")
    elif pos[0] <= 0:
        movement = [movement[0] * -1, movement[1]]
    elif pos[1] <= 0:
        movement = [movement[0], movement[1] * -1]
    elif lopta in overlap:
        movement = bounce(pos, desk_pos)
    canvas.after(4, pohyb)
def mover(e):
    global x
    x2 = e.x
    if x != 0:
        mouse = x2 - x
        canvas.move(desk, mouse, 0)
        x = e.x
def bounce(lopta_pos, rec_pos):
    lopta_pos = (lopta_pos[0] + lopta_pos[2]) // 2
    rec_middle = (rec_pos[0] + rec_pos[2]) // 2
    lopta_to_rec = lopta_pos - rec_middle
    return [lopta_to_rec // (rec_w // 3), -1]
root = tk.Tk()
width = 1000
height = 700
ws = 100
brick_w = 100
brick_h = 30
bricks_x = 10
bricks_y = 4
bricks = []
rec_w = 100
canvas = tk.Canvas(root, width=width, height=height, bg='black')
canvas.pack()
farby = ['red', 'yellow', 'purple', 'lime']
dom = ['white', 'green', 'pink', 'indigo', 'gray']
movement = [0, 1]
lopta = canvas.create_oval(width // 2 - ws, height // 2 - ws, width // 2 + ws, height // 2 + ws, fill=random.choice(farby))
desk = canvas.create_rectangle(width // 2 - rec_w, height - 30, width // 2 + rec_w, height - 20, fill=random.choice(dom))
start_text = canvas.create_text(width // 2, height // 2 - 50,text='Klikni na dosku pre spustenie', fill=random.choice(dom))

def destroy_brick():
    global movement
    global chance
    coords_lopta = canvas.coords(lopta)
    items_list = canvas.find_overlapping(coords_lopta[0], coords_lopta[1], coords_lopta[2], coords_lopta[3])
    x_overlap = (coords_lopta[0] + coords_lopta[2]) / 2
    y_overlap = (coords_lopta[1] + coords_lopta[3]) / 2
    top = canvas.find_overlapping(x_overlap, coords_lopta[1], x_overlap + 1, coords_lopta[1])
    bottom = canvas.find_overlapping(x_overlap, coords_lopta[3], x_overlap + 1, coords_lopta[3])
    left = canvas.find_overlapping(coords_lopta[0], y_overlap, coords_lopta[0], y_overlap + 1)
    right = canvas.find_overlapping(coords_lopta[2], y_overlap, coords_lopta[2], y_overlap + 1)
    print(items_list)
    p = 0
    for i in items_list:
        if i in bricks:
            if chance >= 30:
                canvas.create_text(width // 2, height // 2 + 50, text='ENLARGE')
                bricks.remove(i)
                canvas.delete(i)
                resize_desk()
                chance -= 1
                movement[0] *= -1
                print(chance)
            elif chance < 30:
                bricks.remove(i)
                canvas.delete(i)
                resize_desk()
                print('powerup')
                movement[0] *= -1
            else:
                if i in top or i in bottom:
                    if p == 0:
                        bricks.remove(i)
                        canvas.delete(i)
                        movement[1] *= -1
                        chance = randrange(1, 50)
                        p += 1
                    elif i in left or i in right:
                        if p == 0:
                            bricks.remove(i)
                            canvas.delete(i)
                            movement[0] *= -1
                            chance = randrange(1, 50)
                            p += 1
def create_bricks():
    colours = colours = ['red', 'turquoise', 'yellow', 'blue', 'lime']
    for y in range(bricks_y):
        for x in range(bricks_x):
            bricks.append(
                canvas.create_rectangle(x * brick_w, y * brick_h, x * brick_w + brick_w, y * brick_h + brick_h,
                                        fill=colours[y % len(colours)], width=5, outline='black'))
chance = 0
def resize_desk():
    if chance >= 30:
        coords = canvas.coords(desk)
        coords[0] *= 2
        canvas.coords(desk, coords)
    else:
        coords = canvas.coords(desk)
        coords[0] = width // 2 - rec_w
        canvas.coords(desk, coords)
canvas.bind('<Button-1>', starter)
canvas.bind('<Motion>', mover)
create_bricks()
root.mainloop()
