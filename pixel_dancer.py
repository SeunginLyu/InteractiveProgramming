import pygame
import numpy
import random

'''Global variable declaration'''

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME PRESETS
NUM_BG = 8
NUM_X = 4
NUM_Y = 4
NUM_MONSTER = 5
TOTAL_GRID = NUM_X * NUM_Y
FPS = 60  # frames(while loops) per second

#ENERGY PRESETS
MAX_ENERGY = 100
ENERGY_CONSTANT = 120  # energy lasts ENERGY_CONSTANT seconds
DAMAGE = int(0.1 * MAX_ENERGY)
BONUS = int(0.2 * MAX_ENERGY)
MARGINAL_ERROR = 10  # 10 frames

# MUSIC PRESETS
MUSIC = 'Ghost_fight.mp3'
BEAT_CONST = 64  # arbitrary Frames/BEAT


class Grid(object):
    '''This class represents a single grid in the game canvas'''
    def __init__(self, row, col, location, length, width, image,
                 alpha=256):
        self.row = row  # relative row number in a gridlist
        self.col = col  # relative col number in a gridlist
        self.length = length
        self.width = width
        self.location = location  # absolute location (pixels)
        self.image = image
        self.alpha = alpha  # transparency


class GridList(object):
    '''This class represents the list of all the grids'''
    def __init__(self, num_rows, num_cols, grid_size, name_list, pic_num):
        self.name_list = name_list
        self.pic_num = pic_num
        self.pic = pygame.image.load(self.name_list[self.pic_num])
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid_size = grid_size
        self.colored_grid_count = 0
        self.chop_image()

    def new_grid(self,image):
        '''Updates the grid to previous background picture'''
        self.pic = image
        self.chop_image()

    def chop_image(self):
        '''Chops original image and gives them to individual grids'''
        length = self.grid_size[0] / self.num_cols  # length of individual grid
        width = self.grid_size[1] / self.num_rows  # width of individual grid
        grid = []
        for i in range(self.num_rows):
            grid_row = []
            for j in range(self.num_cols):
                chop_num =  0
                grid_pic = self.pic
                small_row = self.num_rows
                small_col = self.num_cols
                while chop_num < self.num_rows-1:
                    chop_j, chop_i = self.find_chop_ij(j,i,small_col,small_row)
                    location_x = int((self.grid_size[1] / self.num_cols) * chop_j)
                    location_y = int((self.grid_size[0] / self.num_rows) * chop_i)
                    grid_pic = pygame.transform.chop(grid_pic,(location_x,location_y,length,width))
                    small_col -= 1
                    small_row -= 1
                    chop_num += 1
                location_x = int((self.grid_size[1] / self.num_cols) * j)
                location_y = int((self.grid_size[0] / self.num_rows) * i)
                location = (location_x, location_y)
                new_grid = Grid(i, j, location, length, width, grid_pic)
                grid_row.append(new_grid)
                file_name = str(i+0.1*j) +'.svg'
            grid.append(grid_row)
        self.gridlist = numpy.array(grid)

    def find_chop_ij(self, j,i,num_cols,num_rows):
        '''returns the number of the grid to be chopped'''
        j = j+1
        i = i+1
        if j >= num_cols:
            j = 0
        if i >= num_rows:
            i = 0
        return (j,i)


class GridListViewer(object):
    '''This class displays the grids to be cleared'''
    def __init__(self, screen, grid_list):
        num_rows = grid_list.num_rows
        num_cols = grid_list.num_cols
        for i in range(num_cols):
            for j in range(num_rows):
                grid = grid_list.gridlist[j, i]
                image = grid.image
                image.set_alpha(grid.alpha)
                screen.blit(image, grid.location)


class Background:
    '''This class represents the background image'''
    def __init__(self, name_list, num):
        self.name_list = name_list
        self.num = num
        self.pic = pygame.image.load(self.name_list[self.num])

    def new_background(self):
        '''Updates the background to a new random image'''
        new_num = random.randint(1,NUM_BG)
        while new_num == self.num:
            new_num = random.randint(1,NUM_BG)
        self.num = new_num
        self.pic = pygame.image.load(self.name_list[self.num])


class BackgroundViewer:
    '''This class displays the background'''
    def __init__(self, screen, background):
        screen.blit(background.pic, (0, 0))


class Player:
    '''This class represents the player that the user controls'''
    def __init__(self, name, place):
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic, 0,
                                             1/min(NUM_X, NUM_Y)*2)
        self.place = (place[0], place[1])
        self.flipped = False
        self.energy = MAX_ENERGY
        self.has_energy_decreased = False

    def move(self, dx, dy, grid, beat):
        '''Moves the player according to keyboard input and changes grid color'''
        gridlist = grid.gridlist
        x = self.place[0]+dx
        y = self.place[1]+dy
        if (dx == 1 or dy == 1) and not self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = True
        if (dx == -1 or dy == -1) and self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = False
        if x < 0 or x >= NUM_X or y < 0 or y >= NUM_Y:  # OUT of GRID
            x = 0
            y = 0
            self.decrease_energy()
        if gridlist[x][y].alpha == 256 and not beat:  # OFF-BEAT
            gridlist[x][y].alpha /= 2
            self.decrease_energy()
        elif (gridlist[x][y].alpha == 256 and beat) or (gridlist[x][y].alpha != 0 and gridlist[x][y].alpha != 256):
            gridlist[x][y].alpha = 0
            grid.colored_grid_count += 1
        self.place = (x, y)

    def get_absolute_location(self, gridlist):
        '''Returns the absolute location of the player'''
        absolute_x = gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x, absolute_y)

    '''The following functions handle player-related energy change'''
    def update_energy(self):
        dx = MAX_ENERGY / FPS / ENERGY_CONSTANT
        self.energy = self.energy - dx

    def decrease_energy(self):
        self.energy = self.energy - DAMAGE
        self.has_energy_decreased = True

    def increase_energy(self):
        self.energy = self.energy + BONUS


class PlayerKeyController():
    '''This class is the player controller'''
    def __init__(self, event, player, grid, beat, monster):
        if event.key == pygame.K_RIGHT:
            player.move(0, 1, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_LEFT:
            player.move(0, -1, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_UP:
            player.move(-1, 0, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_DOWN:
            player.move(1, 0, grid, beat)
            collision = CollisionHandler(player, monster)


class BeatHandler():
    '''This class checks whether the player follows the beat'''
    def __init__(self, loop_num, BEAT_CONST, MARGINAL_ERROR):
        beat_rate = loop_num % BEAT_CONST
        if beat_rate < MARGINAL_ERROR or BEAT_CONST-beat_rate < MARGINAL_ERROR:
            self.flag = True
        else:
            self.flag = False


class PlayerViewer:
    '''This class displays the player'''
    def __init__(self, screen, player, grid):
        screen.blit(player.pic, player.get_absolute_location(grid.gridlist))


class MessageViewer:
    '''This class displays any message'''
    def __init__(self, screen, font, font_size, message, msg_location,
                 color=WHITE):
        myfont = pygame.font.SysFont(font, font_size, True)
        label = myfont.render(message, True, color)
        screen.blit(label, msg_location)


class RhythmViewer:
    '''This class displays the rhythm viewer at the bottom'''
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
    '''This class displays the energy state on the right'''
    def __init__(self, screen, player):
        if(player.has_energy_decreased):
            r = random.randint(0, 255)
            color = (r, 0, 0)
        else:
            color = BLUE
        screen_size = screen.get_rect().size
        length = 100
        height = screen_size[1]-100
        current_energy = player.energy

        image = pygame.Surface((length, height))
        image2 = pygame.Surface((length, height))
        box_padding = 20
        if(current_energy >= 0):
            dy = int(height * (MAX_ENERGY-current_energy) / MAX_ENERGY)
        else:
            dy = height
        # Decreased ENERGY
        box1_x = length - 100
        box1_y = 0
        rect1 = pygame.Rect(box1_x+0.5*box_padding,
                            box1_y, 100-box_padding, dy)
        pygame.draw.rect(image, WHITE, rect1)
        image.set_alpha(0)  # lost energy is transparent

        # ENERGY LEFT
        box2_x = box1_x
        box2_y = dy
        rect2 = pygame.Rect(box2_x+0.5*box_padding, box2_y, 100-box_padding,
                            screen_size[0] - dy)
        pygame.draw.rect(image2, color, rect2)
        screen.blit(image, (screen_size[0]-length, 0))
        screen.blit(image2, (screen_size[0]-length, 0))


class Monster:
    '''This class represents the monsters(chocolates)'''
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
        self.mode = 0

    def randomize(self):
        '''Spawns the monsters at random spots'''
        self.monsterlist = []
        for i in range(self.num_monster):
            x = random.randint(0, self.max_x-1)
            y = random.randint(0, self.max_y-1)
            while (x,y) in self.monsterlist:
                x = random.randint(0, self.max_x-1)
                y = random.randint(0, self.max_y-1)
            self.monsterlist.append((x, y))


class MonsterViewer:
    '''This class displays the monsters'''
    def __init__(self, screen, monster, grid):
        if monster.mode == 1:
            pic = monster.pic1
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic, current_grid.location)
        else:
            pic = monster.pic2
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic, current_grid.location)


class CollisionHandler():
    '''This class checks if the player collides with a monster'''
    def __init__(self, player, monsters):
        self.flag = False
        player_location = player.place
        for monster_location in monsters.monsterlist:
            if player_location == monster_location and monsters.mode == 1:
                self.flag = True
                break
        if (self.flag):
            player.decrease_energy()


def main():
    # initializing pygame
    pygame.init()

    # Game Settings
    pygame.display.set_caption('PIXEL DANCER')
    start = True
    gameover = False
    while (start and not gameover):
        # initializing background / determining canvas_size
        name_list = ['black.png','insta1.jpg','insta2.jpg','insta3.jpg','insta4.jpg','insta5.jpg','insta6.jpg','insta7.jpg','insta8.jpg']
        bg = Background(name_list,random.randint(1,8))
        grid_size = bg.pic.get_rect().size
        canvas_size = (grid_size[0]+100, grid_size[1]+100)

        # initializing player
        player = Player('player.png', (0, 0))

        # initializing Monster
        monster = Monster('choco.png', 'warning.png', NUM_X, NUM_Y,
                          NUM_MONSTER, canvas_size)

        # initializing screen & grid & clock
        screen = pygame.display.set_mode(canvas_size)
        grid_list = GridList(NUM_X, NUM_Y, grid_size, name_list, 0)
        clock = pygame.time.Clock()
        loop_num = 0
        is_matching = True
        total_num_pic = 0

        # plays background music, BPM is about 110
        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.play(-1)
        start = False
        running = True

        while running:
            # instatiate new background and new grids
            if grid_list.colored_grid_count == TOTAL_GRID:
                player.increase_energy()
                total_num_pic += 1
                grid_list.colored_grid_count = 0
                grid_list.new_grid(bg.pic)
                bg.new_background()

            #  checks exteral inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    is_matching = BeatHandler(loop_num, BEAT_CONST,
                                              MARGINAL_ERROR).flag
                    player_controller = PlayerKeyController(event, player, grid_list,
                                                            is_matching, monster)
            player.update_energy()  # constantly decrease enrgy every frame
            if(loop_num % BEAT_CONST == 0):  # initialize the attribute every beat
                player.has_energy_decreased = False
            elif(not player.has_energy_decreased):
                collision = CollisionHandler(player, monster)

            # initializing viewers
            background_viewer = BackgroundViewer(screen, bg)
            grid_viewer = GridListViewer(screen, grid_list)
            if loop_num % (BEAT_CONST*2) < BEAT_CONST:
                monster.mode = 1
                monster_viewer = MonsterViewer(screen, monster, grid_list)
            elif loop_num % BEAT_CONST == 0:
                monster.randomize()
                monster.mode = 2
                player.energy_color = BLUE
            else:
                monster_viewer = MonsterViewer(screen, monster, grid_list)
            player_viewer = PlayerViewer(screen, player, grid_list)
            energy_viewer = EnergyViewer(screen, player)
            rhythm_viewer = RhythmViewer(screen, BEAT_CONST, loop_num,
                                         MARGINAL_ERROR)

            loop_num += 1
            clock.tick(FPS)
            pygame.display.flip()

            if player.energy <= 0:
                running = False
                gameover = True
        screen = pygame.display.set_mode(canvas_size)
        while(gameover):

            font = "norasi"
            font_size = 80
            msg = "GAME OVER"
            msg_location = (90, 80)

            font_size2 = 30
            msg2 = "PRESS ENTER TO PLAY AGAIN"
            msg_location2 = (90, 480)

            font_size3 = 50
            msg3 = "Pictures Cleared : " + str(total_num_pic)
            msg_location3 = (90, 280)
            gameover_message = MessageViewer(screen, font, font_size, msg,
                                             msg_location, RED)
            gameover_message2 = MessageViewer(screen, font, font_size2, msg2,
                                              msg_location2, BLUE)
            gameover_message3 = MessageViewer(screen, font, font_size3, msg3,
                                              msg_location3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameover = False
                        start = True
            clock.tick(FPS)
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
