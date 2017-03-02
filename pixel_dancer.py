import pygame
import numpy
import random

'''Global variable declaration'''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# GAME PRESETS
NUM_X = 6
NUM_Y = 6
TOTAL_GRID = NUM_X * NUM_Y
FPS = 60  # frames(while loops) per second
MAX_ENERGY = 100


class Grid(object):
    '''This class represents a single grid in the game canvas'''
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
    '''This class represents the list of all the grids'''
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
        self.energy = MAX_ENERGY

    def move(self, dx, dy, grid, beat):
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
        if gridlist[x][y].alpha == 256 and not beat:
            gridlist[x][y].alpha /= 2
        elif (gridlist[x][y].alpha == 256 and beat) or (gridlist[x][y].alpha != 0 and gridlist[x][y].alpha != 256):
            gridlist[x][y].alpha = 0
            grid.colored_grid_count += 1
        self.place = (x, y)

    def get_absolute_location(self, gridlist):
        absolute_x = gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x, absolute_y)

    def update_energy(self, loop_num, beat_constant):
        dx = int(loop_num / beat_constant) / MAX_ENERGY
        self.energy = self.energy - dx


class PlayerKeyController():
    def __init__(self, event, player, grid, beat):
        if event.key == pygame.K_RIGHT:
            player.move(0, 1, grid, beat)
        if event.key == pygame.K_LEFT:
            player.move(0, -1, grid, beat)
        if event.key == pygame.K_UP:
            player.move(-1, 0, grid, beat)
        if event.key == pygame.K_DOWN:
            player.move(1, 0, grid, beat)


class BeatHandler():
    def __init__(self, loop_num, BEAT_CONST, MARGINAL_ERROR):
        if (loop_num % BEAT_CONST) < MARGINAL_ERROR or (BEAT_CONST-loop_num % BEAT_CONST) < MARGINAL_ERROR:
            self.flag = True
        else:
            self.flag = False


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
    def __init__(self, screen, rhythm, loop_num, marginal_error):
        screen_size = screen.get_rect().size
        length = screen_size[0]-100
        height = 100
        image = pygame.Surface((length, height))
        # drawing line
        line_start = (0, int(height / 2))
        line_end = (length, int(height / 2))
        line_width = 3
        pygame.draw.line(image, WHITE, line_start, line_end, line_width)

        # drawing two circles
        radius = 40
        dx = ((length) - 2*radius) / rhythm / 2
        pos = (int(line_start[0]+radius+dx*(loop_num % rhythm)), line_start[1])
        pos2 = (int(length-radius-dx*(loop_num % rhythm)),
                line_start[1])
        center = int(length / 2)
        if(abs(pos[0] - center) <= marginal_error/10 * dx):
            color = RED
            width = 6
        elif(abs(pos[0] - center) < marginal_error*dx):
            color = BLUE
            width = 6
        else:
            color = WHITE
            width = 3
        pygame.draw.circle(image, color, pos, radius, width)
        pygame.draw.circle(image, color, pos2, radius, width)
        screen.blit(image, (0, screen_size[1]-height))


class EnergyViewer:
    def __init__(self, screen, player):
        screen_size = screen.get_rect().size
        length = 100
        height = screen_size[1]-100
        current_energy = player.energy

        image = pygame.Surface((length, height))
        image2 = pygame.Surface((length, height))
        image2.fill(WHITE)
        box_padding = 20

        # Decreased ENERGY
        box1_x = length - 100
        box1_y = 0
        dy = int(height / MAX_ENERGY) * (MAX_ENERGY - current_energy)
        # drawing two rectangles
        rect1 = pygame.Rect(box1_x+0.5*box_padding,
                            box1_y, 100-box_padding, dy)
        pygame.draw.rect(image, WHITE, rect1)
        image.set_alpha(0)  # lost energy is transparent

        # ENERGY
        box2_x = box1_x
        box2_y = dy
        rect2 = pygame.Rect(box2_x+0.5*box_padding, box2_y, 100-box_padding,
                            screen_size[0] - dy)

        pygame.draw.rect(image2, YELLOW, rect2)
        screen.blit(image, (screen_size[0]-length, 0))
        screen.blit(image2, (screen_size[0]-length, 0))

class Monster:
    def __init__(self,name1,name2,max_x,max_y,num_monster,canvas_size):
        self.max_x = max_x
        self.max_y = max_y
        self.num_monster = num_monster
        self.pic1 = pygame.image.load(name1)
        self.pic1 = pygame.transform.rotozoom(self.pic1, 0,
                                             1/min(NUM_X, NUM_Y)*2)
        self.pic2 = pygame.image.load(name2)
        self.pic2 = pygame.transform.rotozoom(self.pic2, 0,
                                             1/min(NUM_X, NUM_Y)*0.7)
        self.monsterlist = []

    def randomize(self):
        self.monsterlist = []
        for i in range(self.num_monster):
            x = random.randint(0,self.max_x-1)
            y = random.randint(0,self.max_y-1)
            while (x,y) in self.monsterlist:
                x = random.randint(0,self.max_x-1)
                y = random.randint(0,self.max_y-1)
            self.monsterlist.append((x,y))

class MonsterViewer:
    def __init__(self, screen, monster ,grid, mode):
        if mode == 1:
            pic = monster.pic1
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic,current_grid.location)
        else:
            pic = monster.pic2
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic,current_grid.location)

def main():

    # initializing pygame
    pygame.init()

    # Game Settings
    pygame.display.set_caption('PIXEL DANCER')
    # initializing background / determining canvas_size
    bg = Background('square.jpg')
    grid_size = bg.pic.get_rect().size
    canvas_size = (grid_size[0]+100, grid_size[1]+100)
    # initializing player
    player = Player('player.png', (0, 0))

    # initializing Monster
    num_monster = 5
    monster = Monster('choco.png','warning.png',NUM_X, NUM_Y,num_monster,canvas_size)

    # initializing screen & grid & clock
    screen = pygame.display.set_mode(canvas_size)
    grid = GridList(NUM_X, NUM_Y, grid_size)
    clock = pygame.time.Clock()
    loop_num = 0

    # plays background music, BPM is about 110
    pygame.mixer.music.load('Ghost_fight.mp3')
    pygame.mixer.music.play(-1)
    BEAT_CONST = 64  # arbitrary Frames/second value proportional to BPM
    MARGINAL_ERROR = 10  # 10 frames
    is_matching = True
    running = True
    while running:
        #  checks exteral inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                is_matching = BeatHandler(loop_num, BEAT_CONST,
                                          MARGINAL_ERROR).flag
                player_controller = PlayerKeyController(event, player, grid,
                                                        is_matching)

        player.update_energy(loop_num, BEAT_CONST)
        # initializing viewers
        background_viewer = BackgroundViewer(screen, bg)
        grid_viewer = GridListViewer(screen, grid)
        if loop_num % (BEAT_CONST*2) < BEAT_CONST:
            monster_viewer = MonsterViewer(screen, monster, grid, 1)
        elif loop_num % BEAT_CONST == 0:
            monster.randomize()
        else:
            monster_viewer = MonsterViewer(screen, monster, grid, 2)
        player_viewer = PlayerViewer(screen, player, grid)
        energy_viewer = EnergyViewer(screen, player)
        rhythm_viewer = RhythmViewer(screen, BEAT_CONST, loop_num,
                                     MARGINAL_ERROR)

        if grid.colored_grid_count == TOTAL_GRID:  # when all grids are colored
            font = "norasi"
            font_size = 50
            msg = "THIS IS NOT OVER"
            msg_location = (50, 80)
            end_message_viewer = MessageViewer(screen, font, font_size, msg,
                                               msg_location)
        loop_num += 1
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
