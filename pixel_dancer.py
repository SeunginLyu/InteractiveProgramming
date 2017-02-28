import pygame
import numpy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Grid(object):
    def __init__(self, row, col, location, length, width, color=BLACK,
                 alpha=200):
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
                image.fill(grid.color)
                screen.blit(image, grid.location)


class Background:
    def __init__(self,name):
        self.pic = pygame.image.load(name)
        print (self.pic.get_rect().size)


class PygameKeyboardController:
    def __init__(self,model):
        self.model = model

    def handle_key_event(self,evemt):
        if event.type != pygame.keydown:
            return
        if event.type == pygame.K_LEFT:
            self.model.paddle.x += -10

class Player:
    def __init__(self,name,place):
        self.pic = pygame.image.load(name)
        self.place = place

    def move(self):
        pass

def main():
    pygame.init()
    pygame.display.set_caption('Artist')
    bg = Background('square.jpg')
    canvas_size = bg.pic.get_rect().size
    screen = pygame.display.set_mode(canvas_size)
    grid = GridList(3, 3, canvas_size)  # row n by col n gridlist
    print(grid.gridlist)
    done = False
    while not done:

        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done so we exit this loop
        screen.blit(bg.pic, (0, 0))
        player = Player('player.png', (canvas_size[0]*3/5, canvas_size[1]*3/5))
        screen.blit(player.pic, player.place)
        grid_viewer = GridListViewer(screen, grid)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
