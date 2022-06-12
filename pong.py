import readchar as rc
from time import sleep

def init(width, height):
    global paddle_length
    array = []
    for i in range(width):
        array.append([1 if i < paddle_length else 0])
        for j in range(height):
            array[i].append(0)
    return array

def update(array, width, height, key):
    global paddle_length
    global paddle_x
    for i in range(width):
        for j in range(height):
            if array[i][j] == 1: # paddle movement
                if key == 'w':
                    for c in range(paddle_length):
                        array[c][j+j] = 0
                elif key == 's':
                    paddle_x += 1
                    for c in range(j, paddle_length):
                        array[c][j+j] = 0
                    for c in range(j, paddle_length):
                        array[(c+paddle_x)%width][(j+j)%height] = 1
                    return array
    return array

def draw(array, width, height):
    print("\033[2J")
    for i in range(width):
        for j in range(height):
            print(array[i][j], end='')
        print()

resolution_x = 15
resolution_y = 50
paddle_length = resolution_y//10
paddle_x = 0
display = init(resolution_x, resolution_y)

c = ""
while (c != 'q'):
    draw(display, resolution_x, resolution_y)
    c = rc.readkey()
    display = update(display, resolution_x, resolution_y, c)
    sleep(0.1)