from threading import main_thread
import pygame, sys, math, time

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400

def main():
    global SCREEN, CLOCK
    
    pygame.init()
    
    pygame.display.set_caption('Snake Path')


    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    spiral(7)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    


def drawGrid():
    blockSize = 20 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

# def tspiral(startX, startY, moves):
#     # Direction (dir) can either be clockwise or counterclockwise
#     x = (startX+9)*20
#     y = (startY+9)*20
#     print(x, y)
    

def spiral(move):
    X= 100
    Y = 100
    x = y = 0 # starts at origin
    dx = 0
    dy = -1
    counter = -1
    for i in range(max(X, Y)**2):
        if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
            print(x, y)
            counter += 1
            pygame.draw.rect(SCREEN, RED, ((x+9)*20,(y+9)*20, 20, 20))
            pygame.display.update() 
            pygame.time.wait(600)
            if counter == move:
                print('Move', move, 'is at (', x, ',', y, ')')
                return
        if (x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y)):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy

main() # runs program



