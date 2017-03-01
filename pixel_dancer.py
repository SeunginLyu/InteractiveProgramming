import pygame
import numpy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
NUM_X = 6
NUM_Y = 6
TOTAL_GRID = NUM_X * NUM_Y


class Grid(object):
    def __init__(self, row, col, location, length, width, color=BLACK,
                 alpha=256):
        self.row = row  # relative row number in a gridlist
        self.col = col  # relative col number in a gridlist
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
        self.colored_grid_count = 0
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
                # if (i+j) % 2 == 0:
                #    color = BLACK
                # else:
                #    color = WHITE
                image.fill(grid.color)
                screen.blit(image, grid.location)


class Background:
    def __init__(self, name):
        self.pic = pygame.image.load(name)


class BackgroundViewer:
    def __init__(self, screen, background):
        screen.blit(background.pic, (0, 0))


class Player:
    def __init__(self, name, place):
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic, 0,
                                             1/min(NUM_X, NUM_Y)*2)
        self.place = (place[0], place[1])
        self.flipped = False

    def move(self, dx, dy, grid):
        gridlist = grid.gridlist
        x = self.place[0]+dx
        y = self.place[1]+dy
        if (dx == 1 or dy == 1) and not self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = True
        if (dx == -1 or dy == -1) and self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = False
        if x < 0 or x >= NUM_X or y < 0 or y >= NUM_Y:
            x = 0
            y = 0
        if gridlist[x][y].alpha == 256:
            gridlist[x][y].alpha /= 2
        elif gridlist[x][y].alpha != 0:
            gridlist[x][y].alpha = 0
            grid.colored_grid_count += 1
        self.place = (x, y)

    def get_absolute_location(self, gridlist):
        absolute_x = gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x, absolute_y)


class PlayerKeyController():
    def __init__(self, event, player, grid):
        if event.key == pygame.K_RIGHT:
            player.move(0, 1, grid)
        if event.key == pygame.K_LEFT:
            player.move(0, -1, grid)
        if event.key == pygame.K_UP:
            player.move(-1, 0, grid)
        if event.key == pygame.K_DOWN:
            player.move(1, 0, grid)


class PlayerViewer:
    def __init__(self, screen, player, grid):
        screen.blit(player.pic, player.get_absolute_location(grid.gridlist))


class MessageViewer:
    def __init__(self, screen, font, font_size, message, msg_location,
                 color=WHITE):
        myfont = pygame.font.SysFont(font, font_size, True)
        label = myfont.render(message, True, color)
        screen.blit(label, msg_location)


class RhythmViewer:
    def __init__(self, screen, rhythm):
        screen_size = screen.get_rect().size

        # drawing line
        line_start = (0, screen_size[1]-50)
        line_end = (screen_size[0], screen_size[1]-50)
        line_width = 3
        pygame.draw.line(screen, WHITE, line_start, line_end, line_width)

        # drawing two circles


def main():
    # initializing pygame
    pygame.init()

    # Game Settings
    pygame.display.set_caption('PIXEL DANCER')
    # initializing background / determining canvas_size
    bg = Background('square.jpg')
    canvas_size = bg.pic.get_rect().size
    canvas_size2 = (canvas_size[0], canvas_size[1]+100)
    # initializing player
    player = Player('player.png', (0, 0))

    # initializing screen & grid & clock
    screen = pygame.display.set_mode(canvas_size)
    rhythm_screen = pygame.display.set_mode(canvas_size2)
    grid = GridList(NUM_X, NUM_Y, canvas_size)
    clock = pygame.time.Clock()

    running = True
    while running:
        #  checks exteral inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_controller = PlayerKeyController(event, player, grid)

        # initializing viewers
        background_viewer = BackgroundViewer(screen, bg)
        grid_viewer = GridListViewer(screen, grid)
        player_viewer = PlayerViewer(screen, player, grid)
        rhythm_viewer = RhythmViewer(rhythm_screen, 10)
        if grid.colored_grid_count == TOTAL_GRID:  # when all grids are colored
            font = "norasi"
            font_size = 50
            msg = "THIS IS NOT OVER"
            msg_location = (50, 80)
            end_message_viewer = MessageViewer(screen, font, font_size, msg,
                                               msg_location)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
