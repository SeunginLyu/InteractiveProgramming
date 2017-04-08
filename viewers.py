import pygame
import random
import config

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


class BackgroundViewer(object):
    '''This class displays the background'''
    def __init__(self, screen, background):
        """
        This should be a draw() method
        """
        screen.blit(background.pic, (0, 0))


class PlayerViewer(object):
    '''This class displays the player'''
    def __init__(self, screen, player, grid):
        screen.blit(player.pic, player.get_absolute_location(grid.gridlist))


class MessageViewer(object):
    '''This class displays any message'''
    def __init__(self, screen, font, font_size,
                 message, msg_location, color=WHITE):
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
