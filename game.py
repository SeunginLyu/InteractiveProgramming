class game():
    def __init__(self, config):
        # initializing background / determining canvas_size


        bg = Background(name_list, random.randint(1, 8))
        grid_size = bg.pic.get_rect().size
        canvas_size = (grid_size[0]+100, grid_size[1]+100)

        # initializing player
        player = Player('./resources/player.png', (0, 0))

        # initializing Monster
        monster = Monster('./resources/choco.png',
                          './resources/warning.png', NUM_X, NUM_Y,
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

    @property
    def
