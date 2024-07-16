from ursina import *
from random import randint
import tkinter as tk

app = Ursina()

snake = Entity(model='cube', texture='assets\\uler', scale=0.5, z=-1, collider='box')
ground = Entity(model='cube', texture='assets\\langit', rotation=(90, 0, 0), scale=(10, 1, 10), z=1)
apple = Entity(model='cube', texture='assets\\apple', scale=0.5, position=(1, -1, -1), collider='mesh')
body = [Entity(model='cube', scale=0.2, texture='assets\\body') for i in range(14)]

camera.orthographic = True
camera.fov = 8

dx = dy = 0
game_over = False

def show_game_over_popup():
    popup = tk.Tk()
    popup.title("Game Over")
    popup.geometry("250x100")

    label = tk.Label(popup, text="Game Over!")
    label.pack(pady=20)

    def restart_game():
        global dx, dy, game_over

        snake.x = 0
        snake.y = 0
        dx = dy = 0
        game_over = False

        popup.destroy()
 
    button = tk.Button(popup, text="Try Again", command=restart_game)
    button.pack()

    popup.mainloop()

hit_sound = Audio("assets/eat.wav", 
                  loop=False, 
                  autoplay=False)

game_over_sound = Audio("assets/crash.mp3",
                        loop=False,
                        autoplay=False)

def update():
    global game_over

    if game_over:
        return

    info = snake.intersects()
    if info.hit:
        apple.x = randint(-9, 9) / 2
        apple.y = randint(-7, 7) / 2
        new = Entity(model='cube', z=-1, scale=0.2, texture='assets\\body')
        body.append(new)
        hit_sound.play()

    for i in range(len(body) - 1, 0, -1):
        pos = body[i - 1].position
        body[i].position = pos

    body[0].x = snake.x
    body[0].y = snake.y

    snake.x += time.dt * dx
    snake.y += time.dt * dy

    if snake.x > 5 or snake.x < -5 or snake.y > 3.9 or snake.y < -3.9:
        game_over = True
        game_over_sound.play()
        show_game_over_popup()
        
def input(key):
    global dx, dy

    for x, y, z in zip(['d', 'a'], [2, -2], [270, 90]):
        if key == x:
            snake.rotation_z = z
            dx = y
            dy = 0

    for x, y, z in zip(['w', 's'], [2, -2], [180, 0]):
        if key == x:
            snake.rotation_z = z
            dy = y
            dx = 0

app.run()
