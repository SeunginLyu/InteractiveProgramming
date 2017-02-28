import pygame
import numpy

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
MAX_X = 6
MAX_Y = 6
TOTAL_GRID = MAX_X * MAX_Y
grid_count = 0

class Grid(object):
    def __init__(self, row, col, location, length, width, color=BLACK,
                 alpha=256):
        self.row = row  # row number in a gridlist
        self.col = col  # col number in a gridlist
        self.length = length
        self.width = width
        self.location = location  # absolute location (pixels)
        self.color = color
        self.alpha = alpha  # transparency

    def __repr__(self):
        return str(self.row) + str(self.col)
        # return str(self.location[0]) + ',' + str(self.location[1])

    def update_grid_color(self, color):
        self.color = color

    def update_grid_alpha(self, color):
        self.color = color

class GridList(object):
    def __init__(self, num_rows, num_cols, grid_size):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid_size = grid_size
        length = grid_size[0] / num_cols  # length of individual grid
        width = grid_size[1] / num_rows  # width of individual grid
        grid = []
        for i in range(num_rows):
            grid_row = []
            for j in range(num_cols):
                location_x = int((grid_size[1] / num_cols) * j)
                location_y = int((grid_size[0] / num_rows) * i)
                location = (location_x, location_y)
                new_grid = Grid(i, j, location, length, width)
                grid_row.append(new_grid)
            grid.append(grid_row)
        self.gridlist = numpy.array(grid)

class GridListViewer(object):
    def __init__(self, screen, grid_list):
        num_rows = grid_list.num_rows
        num_cols = grid_list.num_cols
        for i in range(num_cols):
            for j in range(num_rows):
                grid = grid_list.gridlist[j, i]
                image = pygame.Surface([grid.length, grid.width])
                image.set_alpha(grid.alpha)
                #if (i+j) % 2 == 0:
                #    color = BLACK
                #else:
                #    color = WHITE
                image.fill(grid.color)
                screen.blit(image, grid.location)

class Background:
    def __init__(self,name):
        self.pic = pygame.image.load(name)

class Player:
    def __init__(self,name,place):
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic,0,1/min(MAX_X,MAX_Y)*2)
        self.place = (place[0],place[1])

        self.flipped = False

    def move(self,dx,dy,gridlist):
        global grid_count
        x = self.place[0]+dx
        y = self.place[1]+dy
        if (dx == 1 or dy == 1) and not self.flipped:
            self.pic = pygame.transform.flip(self.pic,True,False)
            self.flipped = True
        if (dx == -1 or dy == -1) and self.flipped:
            self.pic = pygame.transform.flip(self.pic,True,False)
            self.flipped = False
        if x<0 or x>=MAX_X or y<0 or y>=MAX_Y:
            x = 0
            y = 0
        if gridlist[x][y].alpha == 256:
            gridlist[x][y].alpha /=2
        elif gridlist[x][y].alpha != 0:
            gridlist[x][y].alpha = 0
            grid_count += 1
        self.place = (x,y)

    def get_absolute_location(self,gridlist):
        absolute_x = gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x,absolute_y)

def main():
    pygame.init()
    pygame.display.set_caption('PIXEL DANCER')
    bg = Background('square.jpg')
    player = Player('player.png',(0,0))
    canvas_size = bg.pic.get_rect().size
    screen = pygame.display.set_mode(canvas_size)
    grid = GridList(MAX_X, MAX_Y, canvas_size)
    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move(0,1,grid.gridlist)
                if event.key == pygame.K_LEFT:
                    player.move(0,-1,grid.gridlist)
                if event.key == pygame.K_UP:
                    player.move(-1,0,grid.gridlist)
                if event.key == pygame.K_DOWN:
                    player.move(1,0,grid.gridlist)
        screen.blit(bg.pic,(0,0))
        grid_viewer = GridListViewer(screen, grid)
        screen.blit(player.pic,player.get_absolute_location(grid.gridlist))
        if grid_count == TOTAL_GRID:
            myfont = pygame.font.SysFont("norasi", 50, True)
            label = myfont.render("THIS IS NOT OVER!", True, WHITE)
            screen.blit(label, (50,80))
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
