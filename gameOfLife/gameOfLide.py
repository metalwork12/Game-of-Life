import random
import sys
import pygame


class GameOfLife:
    def __init__(self, x ,y, z):
        self.pixelsize =  z
        self.grid = []
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.WINDOW_HEIGHT = x *self.pixelsize
        self.WINDOW_WIDTH = y *self.pixelsize

    def makegrid(self, weighting):
        self.grid = []  # Clear the grid
        for i in range(self.WINDOW_WIDTH//self.pixelsize):
            row = []
            for j in range(self.WINDOW_HEIGHT//self.pixelsize):
                cell = random.randint(0, 20)
                if cell > weighting:
                    row.append(1)
                else:
                    row.append(0)
            self.grid.append(row)

    def makeNewGrid(self):
        return [[0 for _ in range(self.WINDOW_WIDTH//self.pixelsize)] for _ in range(self.WINDOW_HEIGHT//self.pixelsize)]




    def simulateLife(self):
        newgrid = self.makeNewGrid()
        for i in range(self.WINDOW_WIDTH//self.pixelsize):
            for j in range(self.WINDOW_HEIGHT//self.pixelsize):
                count = self.checkCell(i, j)
                if self.grid[i][j] == 1:
                    # Rules for live cells
                    if count < 2 or count > 3:
                        newgrid[i][j] = 0  # Dies
                    else:
                        newgrid[i][j] = 1  # Survives
                else:
                    # Rule for dead cells
                    if count == 3:
                        newgrid[i][j] = 1  # Becomes alive
        self.grid = newgrid


    def checkCell(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.WINDOW_WIDTH//self.pixelsize and 0 <= ny < self.WINDOW_HEIGHT//self.pixelsize:
                    count += self.grid[nx][ny]
        return count

    def drawGrid(self):
        blockSize = self.pixelsize
        for x in range(0, self.WINDOW_WIDTH, blockSize):
            for y in range(0, self.WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                if self.grid[y // blockSize][x // blockSize] == 0:
                    pygame.draw.rect(SCREEN, self.WHITE, rect)
                else:
                    pygame.draw.rect(SCREEN, self.BLACK, rect)

    def drawOnGrid(self):
        self.makegrid(20)
        drawing = False
        while True:
            self.drawGrid()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                if event.type == pygame.MOUSEBUTTONUP:
                    drawing = False


            if drawing:
                self.updateGridWithMouse()

    def updateGridWithMouse(self):
        x, y = pygame.mouse.get_pos()
        dx = x // self.pixelsize
        dy = y // self.pixelsize
        if 0 <= dx < self.WINDOW_WIDTH // self.pixelsize and 0 <= dy < self.WINDOW_HEIGHT // self.pixelsize:
            self.grid[dy][dx] = 1

    def main(self):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        CLOCK = pygame.time.Clock()
        SCREEN.fill(self.BLACK)
        choice = input("would you like to draw om the screen")
        if choice == "yes":
            self.drawOnGrid()
        else:
            self.makegrid(15)

        while True:
            self.drawGrid()
            self.simulateLife()
            pygame.display.update()
            #pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


game = GameOfLife(160, 160, 5)
game.main()

