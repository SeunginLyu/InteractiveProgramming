import pygame


class PlayerController(object):
    '''This class is the player controller'''
    def __init__(self, model):
        self.model = model

    def PlayerKeyController(self, event, grid_list, rhythm):
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
            self.model.move(0, 1, grid_list, rhythm)
        if event.key == pygame.K_LEFT:
            self.model.move(0, -1, grid_list, rhythm)
        if event.key == pygame.K_UP:
            self.model.move(-1, 0, grid_list, rhythm)
        if event.key == pygame.K_DOWN:
            self.model.move(1, 0, grid_list, rhythm)
