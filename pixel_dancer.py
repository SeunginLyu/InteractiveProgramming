"""
Project : Olin College Software Design Spring 2017
By : Seungin Lyu and Yichen Jiang
Game Name : Pixel_Dancer
Version : 0.1
Date : March 8th, 2017

Instruction : Move your doggy around with the arrow keys to paint as many
pictures as possible. Remember, you should follow the music rhythm! If you
aren't following the beat, you will lose your precious energy and end up
only coloring half the grid you are on.  Also, you don't want to go out of the
picture and be careful not to eat the toxic chocolates! You will gain some
extra energy everytime you complete one picture. Good Luck!
(by the way..the energy decreases naturally because doggy is hungry..)
You can play with the game settings by manipulating the defined constants.

Things to FIX:
1) __init__ method of all viewer classes should only specify the self.model
attribute and they should extend it from a basic Viewer class.
Also, draw() methods for each classes should be defined.
Right now the classes aren't technically classes.

2) OOP(Object Oriented Programming) Features for classes such as:
   - Gridlist has Grids.
   - All the different Viewer classes extend default Viwer class.

"""

import pygame
import numpy
import random

'''Global variable declaration'''

# PREDEFINED COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME SETTINGS
NUM_BG = 8  # Number of Background Pictures
NUM_X = 4  # Number of Cols
NUM_Y = 4  # Number of Rows
NUM_MONSTER = 5  # Number of Monsters
TOTAL_GRID = NUM_X * NUM_Y  # Total Number of Grids
FPS = 60  # frames(while loops) per second
MAX_ENERGY = 100  # Maximum Energy for the Doggy
ENERGY_CONSTANT = 120  # energy lasts ENERGY_CONSTANT seconds(maximum)
DAMAGE = int(0.1 * MAX_ENERGY)
BONUS = int(0.2 * MAX_ENERGY)
MARGINAL_ERROR = 10  # the marginal error for following the beat

# MUSIC PRESETS
MUSIC = 'Ghost_fight.mp3'  # the background music
BEAT_CONST = 64  # arbitrary Frames/BEAT constant


class Grid(object):
    '''
    This class represents a single grid in the game canvas.
    '''
    def __init__(self, row, col, location, length, width, image,
                 alpha=256):
        """
        This method initializes the Grid Object

        Precondition : 1) Relative Row, Col number in a gridlist,
                       2) absolute location(pixel) of top-left corner
                       3) length and width
                       4) image(background)
        Postcondition : Grid Object

        """
        self.row = row  # relative row number in a gridlist
        self.col = col  # relative col number in a gridlist
        self.length = length  # length of the grid
        self.width = width  # width of the grid
        self.location = location  # absolute location (pixels)
        self.image = image  # backgrond image
        self.alpha = alpha  # transparency


class GridList(object):
    '''This class represents the list of all the grids'''
    def __init__(self, num_rows, num_cols, grid_size, name_list, pic_num):
        """
        This method initializes the GridList(numpy array) Object

        Precondition : 1) Total number of rows and columns
                       2) Picture Number and the corresponding picture names
                       3) Absolute Pixel Size (x,y) of the gridlist.
        Postcondition : GridList Object (numpy array) that contains a numpy
        array self.gridlist

        """
        #  loads the corresponding picture
        self.name_list = name_list  # list of all the pictures
        self.pic_num = pic_num  # picture refernece number
        self.pic = pygame.image.load(self.name_list[self.pic_num])

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.grid_size = grid_size
        self.colored_grid_count = 0  # number of completely colored grids
        self.chop_image()  # chops the image to cover the old image.

    def new_grid(self, image):
        '''
        Updates the grid image with the previous background picture
        '''
        self.pic = image
        self.chop_image()

    def chop_image(self):
        '''Chops the current image into pieces and assign them to
        individual grids to cover the old image'''
        length = self.grid_size[0] / self.num_cols  # length of individual grid
        width = self.grid_size[1] / self.num_rows  # width of individual grid
        grid = []
        for i in range(self.num_rows):
            grid_row = []
            for j in range(self.num_cols):
                chop_num = 0
                grid_pic = self.pic
                small_row = self.num_rows
                small_col = self.num_cols
                while chop_num < self.num_rows-1:
                    chop_j, chop_i = self.find_chop_ij(j, i, small_col,
                                                       small_row)
                    location_x = int((self.grid_size[1]/self.num_cols)*chop_j)
                    location_y = int((self.grid_size[0]/self.num_rows)*chop_i)
                    grid_pic = pygame.transform.chop(grid_pic,
                                                     (location_x, location_y,
                                                      length, width))
                    small_col -= 1
                    small_row -= 1
                    chop_num += 1
                location_x = int((self.grid_size[1] / self.num_cols) * j)
                location_y = int((self.grid_size[0] / self.num_rows) * i)
                location = (location_x, location_y)
                new_grid = Grid(i, j, location, length, width, grid_pic)
                grid_row.append(new_grid)
            grid.append(grid_row)
        self.gridlist = numpy.array(grid)

    def find_chop_ij(self, j, i, num_cols, num_rows):
        '''
        returns a tuple of number of columns and rows of
        the individual grids to be chopped
        '''
        j = j+1
        i = i+1
        if j >= num_cols:
            j = 0
        if i >= num_rows:
            i = 0
        return (j, i)


class GridListViewer(object):
    '''This class displays the GridList on the screen'''
    def __init__(self, screen, grid_list):
        """
        This should be a draw() method
        """
        num_rows = grid_list.num_rows
        num_cols = grid_list.num_cols
        for i in range(num_cols):
            for j in range(num_rows):
                grid = grid_list.gridlist[j, i]
                image = grid.image
                image.set_alpha(grid.alpha)
                screen.blit(image, grid.location)


class Background(object):
    '''This class represents the background image'''
    def __init__(self, name_list, num):
        self.name_list = name_list
        self.num = num
        self.pic = pygame.image.load(self.name_list[self.num])

    def new_background(self):
        '''Updates the background to a new random image'''
        new_num = random.randint(1, NUM_BG)  # randomly select picture number
        while new_num == self.num:
            new_num = random.randint(1, NUM_BG)
        self.num = new_num
        self.pic = pygame.image.load(self.name_list[self.num])


class BackgroundViewer(object):
    '''This class displays the background'''
    def __init__(self, screen, background):
        """
        This should be a draw() method
        """
        screen.blit(background.pic, (0, 0))


class Player(object):
    '''This class represents the player that the user controls'''
    def __init__(self, name, place):
        """
        This method initializes the Player Object

        Precondition : 1) Name of Player
                       2) Location (x,y) of the Player on GridList Object
        Postcondition : Player Object
        """
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic, 0,
                                             1/min(NUM_X, NUM_Y)*2)
        self.place = (place[0], place[1])
        self.energy = MAX_ENERGY

        # Status Flags
        self.flipped = False
        self.has_energy_decreased = False
        self.has_energy_increased = False

    def move(self, dx, dy, grid_list, beat):
        '''
        Moves the player according dx,dy and changes grid color
        Precondition: 1) dx, dy from generated from PlayerController
                      2) Gridlist that the player is on
                      3) Beat (True if matching, False otherwise)
        Postcondition: the place(location) attribute of the player changes
        '''
        gridlist = grid_list.gridlist
        x = self.place[0]+dx  # new x value after the move
        y = self.place[1]+dy  # new y value after the move

        # Flip Image when moving to the right or up
        if (dx == 1 or dy == 1) and not self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = True

        # Flip Image when moving to the left or down
        if (dx == -1 or dy == -1) and self.flipped:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.flipped = False

        # When Player moves out of Grid, move it back to (0,0)
        if x < 0 or x >= NUM_X or y < 0 or y >= NUM_Y:
            x = 0
            y = 0
            self.decrease_energy()

        # when the player is not following the beat and the grid is not colored
        if gridlist[x][y].alpha == 256 and not beat:
            gridlist[x][y].alpha /= 2
            self.decrease_energy()

        # when the player is following beat and the grid is not colored
        elif (gridlist[x][y].alpha == 256 and beat):
            gridlist[x][y].alpha = 0
            grid_list.colored_grid_count += 1

        # when the player is following beat and the grid is half-colored
        elif (gridlist[x][y].alpha != 0 and gridlist[x][y].alpha != 256):
            gridlist[x][y].alpha = 0
            grid_list.colored_grid_count += 1

        # update the player location
        self.place = (x, y)

    def get_absolute_location(self, gridlist):
        '''
        Returns the absolute location(pixel) of the player
        '''
        absolute_x = gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x, absolute_y)

    '''The following functions handle player-related energy change'''
    def update_energy(self):
        """
        Decreases the enrgy so that it takes "ENERGY_CONSTANT" seconds
        for the energy to naturall decrease to zero if no penalty
        """
        dx = MAX_ENERGY / FPS / ENERGY_CONSTANT
        self.energy = self.energy - dx

    def decrease_energy(self):
        """
        Decreases energy by predefined DAMAGE value
        """
        self.energy = self.energy - DAMAGE
        self.has_energy_decreased = True

    def increase_energy(self):
        """
        Increases energy by predefined BONUS value
        """
        self.energy = self.energy + BONUS
        self.has_energy_increased = True


class PlayerKeyController(object):
    '''This class is the player controller'''
    def __init__(self, event, player, grid, beat, monster):
        """
        Precondition : 1) PyGame event
                       2) player object
                       3) gridlist object
                       4) Beat (True if matching, False otherwise)
                       5) Monster Object
        Postcondition :
        Checks the "key" value and calls player.move() accordingly.
        and handles collision of the player and the monster
        with CollisionHandler object"
        """
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


class BeatHandler(object):
    '''
    This class checks whether the player follows the beat
    '''
    def __init__(self, loop_num, BEAT_CONST, MARGINAL_ERROR):
        """
        Precondition : 1) Loop_num (current frame number)
                       2) BEAT_CONST (predefined frames/beat constant)
                       3) Marginal Error (predefined allowed error of input)
        Postcondition : self.flag is True is following the beat within the
        marginal error, and False otherwise.
        """
        beat_rate = loop_num % BEAT_CONST
        if beat_rate < MARGINAL_ERROR or BEAT_CONST-beat_rate < MARGINAL_ERROR:
            self.flag = True
        else:
            self.flag = False


class PlayerViewer(object):
    '''This class displays the player'''
    def __init__(self, screen, player, grid):
        screen.blit(player.pic, player.get_absolute_location(grid.gridlist))


class MessageViewer(object):
    '''This class displays any message'''
    def __init__(self, screen, font, font_size, message, msg_location,
                 color=WHITE):
        myfont = pygame.font.SysFont(font, font_size, True)
        label = myfont.render(message, True, color)
        screen.blit(label, msg_location)


class RhythmViewer(object):
    '''
    This class displays the rhythm viewer at the bottom
    Two circles move towards the center to represent the beat flow
    '''
    def __init__(self, screen, rhythm, loop_num, marginal_error):
        screen_size = screen.get_rect().size
        length = screen_size[0]-100
        height = 100  # height of the rhythm viewer
        image = pygame.Surface((length, height))

        # drawing the center line
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

        # when the beat is accurate within 0.25 of the marginal error
        if(abs(pos[0] - center) <= marginal_error/5 * dx):
            color = RED
            width = 6

        # when the beat is accurate within the marginal error
        elif(abs(pos[0] - center) < marginal_error*dx):
            color = BLUE
            width = 6

        # when the beat is not matching
        else:
            color = WHITE
            width = 3
        pygame.draw.circle(image, color, pos, radius, width)
        pygame.draw.circle(image, color, pos2, radius, width)
        screen.blit(image, (0, screen_size[1]-height))


class EnergyViewer(object):
    '''
    This class displays the energy state on the right section of the screen
    by drawing two rectangles of heights 1-dy and dy.
    '''
    def __init__(self, screen, player):
        if(player.has_energy_decreased):
            r = random.randint(0, 255)  # generates blinkning of red color
            color = (r, 0, 0)
        if(player.has_energy_increased):
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = (0, g, b)  # generates blinking of yellow color
        else:
            color = BLUE
        screen_size = screen.get_rect().size
        length = 100
        height = screen_size[1]-100
        current_energy = player.energy

        image = pygame.Surface((length, height))
        image2 = pygame.Surface((length, height))
        box_padding = 20

        # when energy is greater than zero
        if(current_energy >= 0):
            dy = int(height * (MAX_ENERGY-current_energy) / MAX_ENERGY)
        # when energy is less than zero
        else:
            dy = height

        # Decreased ENERGY
        box1_x = length - 100
        box1_y = 0
        rect1 = pygame.Rect(box1_x+0.5*box_padding,
                            box1_y, 100-box_padding, dy)
        pygame.draw.rect(image, WHITE, rect1)
        image.set_alpha(0)  # lost energy is transparent

        # Rectangle that represents ENERGY LEFT
        box2_x = box1_x
        box2_y = dy
        rect2 = pygame.Rect(box2_x+0.5*box_padding, box2_y, 100-box_padding,
                            screen_size[0] - dy)
        pygame.draw.rect(image2, color, rect2)
        screen.blit(image, (screen_size[0]-length, 0))
        screen.blit(image2, (screen_size[0]-length, 0))


class Monster(object):
    '''This class represents the monsters(chocolates)'''
    def __init__(self, name1, name2, max_x, max_y,
                 num_monster, canvas_size):
        """
        Precondition : 1) Image name1, name2 for monsters
                       2) Maximum x, y value for the monster Postcondition
                       3) Number of monsters
                       4) Canvas Size
        Postcondition : Monster Object that contains monsterlist[] with
                        randomized monster location
        """
        self.max_x = max_x
        self.max_y = max_y
        self.num_monster = num_monster
        self.pic1 = pygame.image.load(name1)
        self.pic1 = pygame.transform.rotozoom(self.pic1, 0,
                                              1/min(NUM_X, NUM_Y)*2)
        self.pic2 = pygame.image.load(name2)
        self.pic2 = pygame.transform.rotozoom(self.pic2, 0,
                                              1/min(NUM_X, NUM_Y)*0.7)
        self.monsterlist = []  # array that contains monster location
        self.mode = 0  # mode 1 = chocolate, mode 2 = warning sign

    def randomize(self):
        '''
        Spawns the monsters at random spots, saves the randomizes location
        in self.monsterlist[]
        '''
        self.monsterlist = []
        for i in range(self.num_monster):
            x = random.randint(0, self.max_x-1)
            y = random.randint(0, self.max_y-1)
            while (x, y) in self.monsterlist:
                x = random.randint(0, self.max_x-1)
                y = random.randint(0, self.max_y-1)
            self.monsterlist.append((x, y))


class MonsterViewer(object):
    '''This class displays the monsters'''
    def __init__(self, screen, monster, grid):
        # when the monsters are chocolates
        if monster.mode == 1:
            pic = monster.pic1
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic, current_grid.location)
        # when them monsters are warning signs
        else:
            pic = monster.pic2
            for mon_location in monster.monsterlist:
                current_grid = grid.gridlist[mon_location]
                screen.blit(pic, current_grid.location)


class CollisionHandler(object):
    '''This class checks if the player collides with a monster'''
    def __init__(self, player, monsters):
        """
        Precondition : Player object and Monster object
        Postcondition : self.flag = True if the location of each object
        overlaps, self.flag = False otherwise.
        """
        self.flag = False
        player_location = player.place
        # checks all the monster location to see if player is colliding with
        # one of the mosnters
        for monster_location in monsters.monsterlist:
            if player_location == monster_location and monsters.mode == 1:
                self.flag = True
                break

        # if two objects are colliding
        if (self.flag):
            player.decrease_energy()


def main():
    # initializing pygame
    pygame.init()

    # Game Settings
    pygame.display.set_caption('PIXEL DANCER')

    # Default Game Status Flags
    start = True
    gameover = False

    # Loading images & music, creating objects.
    while (start and not gameover):

        # initializing background / determining canvas_size
        name_list = ['black.png', 'insta1.jpg', 'insta2.jpg',
                     'insta3.jpg', 'insta4.jpg', 'insta5.jpg',
                     'insta6.jpg', 'insta7.jpg', 'insta8.jpg']
        bg = Background(name_list, random.randint(1, 8))
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

        # updating game status flags
        start = False
        running = True  # enters the next inner while loop

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
                    is_matching = BeatHandler(loop_num,
                                              BEAT_CONST,
                                              MARGINAL_ERROR).flag
                    player_controller = PlayerKeyController(event,
                                                            player,
                                                            grid_list,
                                                            is_matching,
                                                            monster)
            # constantly decrease enrgy every frame
            player.update_energy()

            # decrease or increase energy only once in per each beat
            if(loop_num % BEAT_CONST == 0):
                player.has_energy_decreased = False
                player.has_energy_increased = False
            # checks if the player collides even if they player doesn't move
            elif(not player.has_energy_decreased):
                collision = CollisionHandler(player, monster)

            # initializing viewers :
            # Background, grid, monster, player, energy, rhythm
            background_viewer = BackgroundViewer(screen, bg)
            grid_viewer = GridListViewer(screen, grid_list)
            # Display chocolates for odd number frames
            if loop_num % (BEAT_CONST*2) < BEAT_CONST:
                monster.mode = 1
                monster_viewer = MonsterViewer(screen, monster, grid_list)

            # Display warning signs for even number frames
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

            # update the loop_num(frame number) and let the time flow
            loop_num += 1
            clock.tick(FPS)
            pygame.display.flip()

            # when the enrgy gets to zero, move on to the gameover while loop
            if player.energy <= 0:
                running = False
                gameover = True

        screen = pygame.display.set_mode(canvas_size)
        while(gameover):

            # displaying messages
            font = "norasi"
            font_size = 80
            msg = "GAME OVER"
            msg_location = (90, 80)

            font_size2 = 30
            msg2 = "PRESS ENTER TO PLAY AGAIN"
            msg_location2 = (90, 480)

            # displays the total number of pictures cleared
            font_size3 = 50
            msg3 = "Pictures Cleared : " + str(total_num_pic)
            msg_location3 = (90, 280)
            gameover_message = MessageViewer(screen,
                                             font,
                                             font_size,
                                             msg,
                                             msg_location,
                                             RED)
            gameover_message2 = MessageViewer(screen,
                                              font,
                                              font_size2,
                                              msg2,
                                              msg_location2,
                                              BLUE)
            gameover_message3 = MessageViewer(screen,
                                              font,
                                              font_size3,
                                              msg3,
                                              msg_location3)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = False

                # go back to the first while loop to start all over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameover = False
                        start = True
            clock.tick(FPS)
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
