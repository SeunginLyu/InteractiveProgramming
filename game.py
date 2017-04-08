import random
import models as m
import pygame


class game():
    def __init__(self, config):
        # initializing background / determining canvas_size
        self.c = config
        self.bg = m.Background(self.c.bg_images,
                               random.randint(1, len(self.c.bg_images))-1)
        self.grid_size = self.bg.pic.get_rect().size
        self.canvas_size = (self.grid_size[0]+100,
                            self.grid_size[1]+100)

        # initializing player & Monster
        self.player = m.Player(self.c.player_image, (0, 0))
        self.monster = m.Monster(self.c.monster_image_1,
                                 self.c.monster_image_2,
                                 self.c.NUM_X,
                                 self.c.NUM_Y,
                                 self.c.NUM_MONSTER,
                                 self.canvas_size)

        # initializing screen & grid & clock
        self.screen = pygame.display.set_mode(self.canvas_size)
        self.grid_list = m.GridList(self.c.NUM_X,
                                    self.c.NUM_Y,
                                    self.grid_size,
                                    self.name_list,
                                    0)
        self.clock = pygame.time.Clock()
        self.frame_count = 0

        self.is_matching = True
        self.total_num_pic = 0

        # plays background music, BPM is about 110
        pygame.mixer.music.load(self.c.MUSIC)
        pygame.mixer.music.play(-1)

    def new_game(self):
        # Default Game Status Flags
        self.start = True
        self.gameover = False

    def start_game(self):
        self.start = False
        self.running = True  # enters the next inner while loop

    def game_over(self):
        self.running = False
        self.gameover = True
