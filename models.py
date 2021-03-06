import numpy
import random
import pygame
import config


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


class Background(object):
    '''This class represents the background image'''
    def __init__(self, name_list, num):
        self.name_list = name_list
        self.num = num
        self.pic = pygame.image.load(self.name_list[self.num])

    def new_background(self):
        '''Updates the background to a new random image'''
        c = config.config()
        new_num = random.randint(1, c.NUM_BG)  # randomly select picture number
        while new_num == self.num:
            new_num = random.randint(1, c.NUM_BG)
        self.num = new_num
        self.pic = pygame.image.load(self.name_list[self.num])


class Player(object):
    '''This class represents the player that the user controls'''
    def __init__(self, name, place):
        """
        This method initializes the Player Object

        Precondition : 1) Name of Player
                       2) Location (x,y) of the Player on GridList Object
        Postcondition : Player Object
        """
        self.c = config.config()
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic, 0,
                                             1/min(self.c.NUM_X,
                                                   self.c.NUM_Y)*2)
        self.place = (place[0], place[1])
        self.energy = self.c.MAX_ENERGY

        # Status Flags
        self.flipped = False
        self.has_energy_decreased = False
        self.has_energy_increased = False

    def move(self, dx, dy, grid_list, rhythm):
        '''
        Moves the player according dx,dy and changes grid color
        Precondition: 1) dx, dy from generated from PlayerController
                      2) Gridlist object that the player is on
                      3) Rhythm object from game class
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
        if x < 0 or x >= self.c.NUM_X or y < 0 or y >= self.c.NUM_Y:
            x = 0
            y = 0
            self.decrease_energy()

        # when the player is not following the beat and the grid is not colored
        if gridlist[x][y].alpha == 256 and not rhythm.is_matching:
            gridlist[x][y].alpha /= 2
            self.decrease_energy()

        # when the player is following beat and the grid is not colored
        elif (gridlist[x][y].alpha == 256 and rhythm.is_matching):
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
        absolute_x = gridlist.gridlist[self.place[0]][self.place[1]].location[0]
        absolute_y = gridlist.gridlist[self.place[0]][self.place[1]].location[1]
        return (absolute_x, absolute_y)

    '''The following functions handle player-related energy change'''
    def update_energy(self):
        """
        Decreases the enrgy so that it takes "ENERGY_CONSTANT" seconds
        for the energy to naturall decrease to zero if no penalty
        """
        dx = self.c.MAX_ENERGY / self.c.FPS / self.c.ENERGY_CONSTANT
        self.energy = self.energy - dx

    def decrease_energy(self):
        """
        Decreases energy by predefined DAMAGE value
        """
        self.energy = self.energy - self.c.DAMAGE
        self.has_energy_decreased = True

    def increase_energy(self):
        """
        Increases energy by predefined BONUS value
        """
        self.energy = self.energy + self.c.BONUS
        self.has_energy_increased = True

    @property
    def has_died(self):
        return self.energy <= 0

    def CollisionHandler(self, monsters):
        """
        Precondition : Player object and Monster object
        Postcondition : self.flag = True if the location of each object
        overlaps, self.flag = False otherwise.
        """
        player_location = self.place
        # checks all the monster location to see if player is colliding with
        # one of the mosnters
        for monster_location in monsters.monsterlist:
            if player_location == monster_location and monsters.mode == 1:
                self.decrease_energy()
                break

    def update(self, rhythm, monsters):
        """
        Updates the player attributes depdending on the current rhythm
        """
        self.update_energy()
        # decrease or increase energy only once in per each beat
        if(rhythm.beat == 0):
            self.has_energy_decreased = False
            self.has_energy_increased = False
        # checks if the player collides even if they player doesn't move
        elif(not self.has_energy_decreased):
            self.CollisionHandler(monsters)


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
        self.c = config.config()
        self.max_x = max_x
        self.max_y = max_y
        self.num_monster = num_monster
        self.pic1 = pygame.image.load(name1)
        self.pic1 = pygame.transform.rotozoom(self.pic1, 0,
                                              1/min(self.c.NUM_X,
                                                    self.c.NUM_Y)*2)
        self.pic2 = pygame.image.load(name2)
        self.pic2 = pygame.transform.rotozoom(self.pic2, 0,
                                              1/min(self.c.NUM_X,
                                                    self.c.NUM_Y)*0.7)
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

    def update(self, rhythm):
        """
        Updates the monster attributes depdending on the current rhythm
        """
        # Display chocolates for odd number frames
        frame_count = rhythm.frame_count
        BEAT_CONST = rhythm.beat_const
        if frame_count % (BEAT_CONST*2) < BEAT_CONST:
            self.mode = 1
        # Display warning signs for even number frames
        elif rhythm.beat == 0:
            self.randomize()
            self.mode = 2


class Message(object):
    """
    This is a message class
    """
    def __init__(self, font, font_size, message, msg_location, color):
        self.font = font
        self.font_size = font_size
        self.message = message
        self.msg_location = msg_location
        self.color = color


class Rhythm(object):
    '''
    This is a Rhythm class that contains attributes that represent
    the concept of 'beat' in this game
    Precondition : 1) frame_count (current frame number)
                   2) BEAT_CONST (predefined frames/beat constant)
                   3) Marginal Error (predefined allowed error of input)
    Postcondition : self.is_matching is True is following the beat within the
    marginal error, and False otherwise.
    '''
    def __init__(self, BEAT_CONST, frame_count, MARGINAL_ERROR):
        self.beat_const = BEAT_CONST
        self.frame_count = frame_count
        self.mg_error = MARGINAL_ERROR
        self.match = self.beat_const/self.mg_error

    def update_frame_count(self, value):
        self.frame_count += value

    @property
    def is_matching(self):
        if self.beat < self.mg_error or (self.beat_const-self.beat) < self.mg_error:
            return True
        else:
            return False

    @property
    def beat(self):
        return self.frame_count % self.beat_const
