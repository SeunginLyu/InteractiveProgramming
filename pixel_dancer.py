"""
Project : Olin College Software Design Spring 2017
By : Seungin Lyu and Yichen Jiang
Game Name : Pixel_Dancer
Version : 0.2
Date : April 7th, 2017

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
import config as c
import game as g

def main():
    # initializing pygame
    pygame.init()

    # Game Settings
    pygame.display.set_caption(c.TITLE)

    # initialize game instance from configuration file
    config = c.config()
    game = g.game(config)
    game.new_game()

    while (game.start and not game.gameover):
        game.start_game()

        while game.running:
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
                    is_matching = BeatHandler(frame_count,
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
            if(frame_count % BEAT_CONST == 0):
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
            if frame_count % (BEAT_CONST*2) < BEAT_CONST:
                monster.mode = 1
                monster_viewer = MonsterViewer(screen, monster, grid_list)

            # Display warning signs for even number frames
            elif frame_count % BEAT_CONST == 0:
                monster.randomize()
                monster.mode = 2
                player.energy_color = BLUE
            else:
                monster_viewer = MonsterViewer(screen, monster, grid_list)
            player_viewer = PlayerViewer(screen, player, grid_list)
            energy_viewer = EnergyViewer(screen, player)
            rhythm_viewer = RhythmViewer(screen, BEAT_CONST, frame_count,
                                         MARGINAL_ERROR)

            # update the frame_count(frame number) and let the time flow
            frame_count += 1
            clock.tick(FPS)
            pygame.display.flip()

            # when the enrgy gets to zero, move on to the gameover while loop
            if player.energy <= 0:
                game.gameover()


        screen = pygame.display.set_mode(canvas_size)
        while(game.gameover):

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
