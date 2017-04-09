"""
Project : Olin College Software Design Spring 2017
By : Seungin Lyu and Yichen Jiang
Game Name : Pixel_Dancer
Version : 0.2
Date : April 8th, 2017

Instruction : Move your doggy around with the arrow keys to paint as many
pictures as possible. Remember, you should follow the music rhythm! If you
aren't following the beat, you will lose your precious energy and end up
only coloring half the grid you are on.  Also, you don't want to go out of the
picture and be careful not to eat the toxic chocolates! You will gain some
extra energy everytime you complete one picture. Good Luck!
(by the way..the energy decreases naturally because doggy is hungry..)
You can play with the game settings by manipulating the defined constants.

"""

import pygame

import game as g
import models as m
import viewers as v
import controllers
import config


def main():
    # initialize pygame
    pygame.init()
    # Game Settings
    c = config.config()
    pygame.display.set_caption(c.TITLE)

    # initialize game instance with impofrted config.py

    while (True):
        # initialize game screen
        game = g.game(c)
        game.new_game()
        screen = pygame.display.set_mode(game.canvas_size)
        # initializes viewers :
        viewers = [v.BackgroundViewer(game.bg),
                   v.GridListViewer(game.grid_list),
                   v.MonsterViewer(game.monster, game.grid_list),
                   v.PlayerViewer(game.player, game.grid_list),
                   v.EnergyViewer(game.player),
                   v.RhythmViewer(game.rhythm)]

        controller = controllers.PlayerController(game.player)
        game.start_game()
        while game.running:

            # checks various game_status
            if game.player.has_died:
                game.game_over()
            if game.is_stage_complete():
                game.set_new_stage()

            #  checks external inputs / runs controllers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    controller.PlayerKeyController(event,
                                                   game.grid_list,
                                                   game.rhythm)
            # updates models every frame (regardless of keyboard input)
            game.monster.update(game.rhythm)
            game.player.update(game.rhythm, game.monster)
            game.rhythm.update_frame_count(1)

            # drawing on screen
            for viewer in viewers:
                viewer.draw(screen)

            game.clock.tick(c.FPS)
            pygame.display.flip()

        # a new screen for gameover screen
        screen = pygame.display.set_mode(game.canvas_size)
        while(game.gameover):
            # initializing models
            font = "norasi"
            msg1 = m.Message(font, 80, "GAME OVER", (90, 80), c.RED)
            msg2 = m.Message(font, 30, "PRESS ENTER TO PLAY AGAIN",
                             (90, 480), c.BLUE)
            msg3 = m.Message(font, 50,
                             "Pictures Cleared : " + str(game.total_num_pic),
                             (90, 280), c.WHITE)
            messages = [msg1, msg2, msg3]

            viewers = []
            # initializing viewers
            for msg in messages:
                viewers.append(v.MessageViewer(msg))

            # drawing on screen
            for viewer in viewers:
                viewer.draw(screen)

            # check external inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game.new_game()

            game.clock.tick(c.FPS)
            pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
