# Game Configuration


class config(object):

    # TITLE
    TITLE = 'PIXEL DANCER'

    # COLOR PRESETS
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
    MARGINAL_ERROR = 15  # the marginal error for following the beat

    # MUSIC PRESETS
    MUSIC = './resources/Ghost_fight.mp3'  # the background music
    BEAT_CONST = 64  # arbitrary Frames/BEAT constant

    # RESOURCE FILES (IMAGES)

    bg_images = ['black.png', 'insta1.jpg', 'insta2.jpg',
                 'insta3.jpg', 'insta4.jpg', 'insta5.jpg',
                 'insta6.jpg', 'insta7.jpg', 'insta8.jpg']
    bg_images = ['./resources/' + file_name for file_name in bg_images]
    player_image = './resources/player.png'
    monster_image_1 = './resources/choco.png'
    monster_image_2 = './resources/warning.png'
