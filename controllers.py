import pygame


class PlayerController(object):
    '''This is the player controller class'''
    def __init__(self, model):
        self.model = model

    def PlayerKeyController(self, event, grid_list, rhythm):
        """
        This function calls the move function of the model
        upon keyboard input from pygame.event
        """
        if event.key == pygame.K_RIGHT:
            self.model.move(0, 1, grid_list, rhythm)
        if event.key == pygame.K_LEFT:
            self.model.move(0, -1, grid_list, rhythm)
        if event.key == pygame.K_UP:
            self.model.move(-1, 0, grid_list, rhythm)
        if event.key == pygame.K_DOWN:
            self.model.move(1, 0, grid_list, rhythm)
