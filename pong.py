import readchar as rc
from time import sleep
from random import randint
from threading import Thread
import sys

def init(height, width):
    global paddle_length
    array = []
    for i in range(height):
        array.append([1 if i < paddle_length else 0]) # left paddle
        for j in range(width):
            array[i].append(0)

    for c in range(paddle_length): # right paddle
        array[c][width-1] = 1

    array[randint((height+4-height), height-4)][randint((width+4-width), width-4)] = 3 # ball    

    return array

def update(height, width, key):
    global paddle_length
    global display
    for i in range(height):
        for j in range(width):
            if display[i][j] == 1: # paddle movement
                if key == 'w':
                    if i == 0:
                        continue                    
                    for c in range(i, (i+paddle_length)):
                        display[c][j] = 0
                        display[c][width-1] = 0
                    for c in range(i, (i+paddle_length)):
                        display[c-1][j] = 1
                        display[c-1][width-1] = 1
                    return
                elif key == 's':
                    if i == height+1-paddle_length:
                        continue
                    for c in range(i, (i+paddle_length)%height):
                        display[c][j] = 0
                        display[c][width-1] = 0
                    for c in range(i, (i+paddle_length)%height):
                        display[c+1][j] = 1
                        display[c+1][width-1] = 1
                    return

def opposite(number):
    return -number

def update_ball(height, width, ball_wait=1):
    global display
    global direction_y
    global direction_x
    global counter

    if counter % ball_wait != 0:
        return

    for i in range(height):
        for j in range(width):
            if display[i][j] == 3:
                if i+direction_y == height:
                    display[i][j] = 0
                    direction_y = opposite(direction_y)
                    display[i+direction_y][j+direction_x] = 3
                    return
                elif i+direction_y == -1:
                    display[i][j] = 0
                    direction_y = opposite(direction_y)
                    display[i+direction_y][j+direction_x] = 3
                    return
                elif j+direction_x == width:
                    restart()
                    return
                elif j+direction_x == -1:
                    restart()
                    return
                elif display[i+direction_y][j+direction_x] == 1:
                    display[i][j] = 0
                    direction_x = opposite(direction_x)
                    display[i+direction_y][j+direction_x] = 3
                    return
                else: 
                    display[i][j] = 0
                    display[i+direction_y][j+direction_x] = 3
                    return

def draw(width, height, symbol):
    print("\033c")
    global display
    for i in range(width):
        for j in range(height):
            if display[i][j] != 0:
                print(symbol, end='')
            else:
                print(' ', end='')
        print("\r")

def get_input():
    global key
    global thread_flag
    while thread_flag:
        key = rc.readkey()

def print_scores(width):
    global score
    print(("Score: " + str(score)).center(width), end="\r")

def restart():
    global score
    global display

    score += 1
    display = init(resolution_x, resolution_y)
    
###############################################################################

resolution_x = 15
resolution_y = 50
paddle_length = resolution_y//10
display = init(resolution_x, resolution_y)
key = ""
thread_flag = True
direction_x = -1 # -1 = left, 1 = right
direction_y = -1 # -1 = down, 1 = up
score = 0
counter = 0

def main():
    global resolution_x
    global resolution_y
    global paddle_length
    global display
    global key
    global thread_flag
    global counter

    p = Thread(target=get_input, args=())

    p.start()
    while (key != 'q'):
        draw(resolution_x, resolution_y, '*')
        update(resolution_x, resolution_y, key)
        key = ""
        update_ball(resolution_x, resolution_y, ball_wait=1)
        print_scores(resolution_y)
        counter += 1
        sleep(0.1)

    thread_flag = False
    p.join()
    sys.exit()

if __name__ == '__main__':
    main()