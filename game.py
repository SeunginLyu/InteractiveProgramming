import random
import models as m
import pygame


class game():
    def __init__(self, config):
        """
        This method initializes all the models in the game class
        """
        # initializing background / determining canvas_size
        self.c = config
        c = self.c
        self.bg = m.Background(c.bg_images,
                               random.randint(1, len(c.bg_images))-1)
        self.grid_size = self.bg.pic.get_rect().size
        self.canvas_size = (self.grid_size[0]+100,
                            self.grid_size[1]+100)

        # initializing player & Monster
        self.player = m.Player(c.player_image, (0, 0))
        self.monster = m.Monster(c.monster_image_1,
                                 c.monster_image_2,
                                 c.NUM_X,
                                 c.NUM_Y,
                                 c.NUM_MONSTER,
                                 self.canvas_size)

        # initializing screen & grid & clock
        self.grid_list = m.GridList(c.NUM_X,
                                    c.NUM_Y,
                                    self.grid_size,
                                    c.bg_images,
                                    0)

        # initializing background music, BPM is about 110
        pygame.mixer.music.load(self.c.MUSIC)
        pygame.mixer.music.play(-1)

        self.frame_count = 0
        self.rhythm = m.Rhythm(c.BEAT_CONST,
                               self.frame_count,
                               c.MARGINAL_ERROR)

        self.total_num_pic = 0  # number of clear pictures(stages)

        # initializing pygame clock
        self.clock = pygame.time.Clock()

    def new_game(self):
        # Default Game Status Flags
        self.start = True
        self.gameover = False
        self.running = False

    def start_game(self):
        self.start = False
        self.running = True  # enters the next inner while loop

    def game_over(self):
        self.running = False
        self.gameover = True

    def is_stage_complete(self):
        return self.grid_list.colored_grid_count == self.c.TOTAL_GRID

    def set_new_stage(self):
        self.player.increase_energy()
        self.total_num_pic += 1
        self.grid_list.colored_grid_count = 0
        self.grid_list.new_grid(self.bg.pic)
        self.bg.new_background()
