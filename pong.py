import readchar as rc
from time import sleep
from random import randint

def init(height, width):
    global paddle_length
    array = []
    for i in range(height):
        array.append([1 if i < paddle_length else 0]) # left paddle
        for j in range(width):
            array[i].append(0)

    for i in range(height): # divider
        array[i][width//2] = 2

    for c in range(paddle_length): # right paddle
        array[c][width-1] = 1

    array[0][width//2] = 3 # ball    

    return array

def update(array, height, width, key):
    global paddle_length
    for i in range(height):
        for j in range(width):
            if array[i][j] == 1: # paddle movement
                if key == 'w':
                    if i == 0:
                        continue                    
                    for c in range(i, (i+paddle_length)):
                        array[c][j] = 0
                        array[c][width-1] = 0
                    for c in range(i, (i+paddle_length)):
                        array[c-1][j] = 1
                        array[c-1][width-1] = 1
                    return array
                elif key == 's':
                    if i == height+1-paddle_length:
                        continue
                    for c in range(i, (i+paddle_length)%height):
                        array[c][j] = 0
                        array[c][width-1] = 0
                    for c in range(i, (i+paddle_length)%height):
                        array[c+1][j] = 1
                        array[c+1][width-1] = 1
                    return array
    return array

def update_ball(array, width, height):
    pass

def draw(array, width, height, symbol):
    print("\033c")
    for i in range(width):
        for j in range(height):
            if array[i][j] != 0:
                print(symbol, end='')
            else:
                print(' ', end='')
        print()

try:
    resolution_x = 15
    resolution_y = 50
    paddle_length = resolution_y//10
    display = init(resolution_x, resolution_y)

    c = ""
    while (c != 'q'):
        print('\033[?25l', end="") # remove cursor
        draw(display, resolution_x, resolution_y, "*")
        c = rc.readkey()
        display = update(display, resolution_x, resolution_y, c)
        sleep(0.1)
except KeyboardInterrupt:
    pass
print('\033[?25h', end="") # show cursor