class PlayerKeyController(object):
    '''This class is the player controller'''
    def __init__(self, event, player, grid, beat, monster):
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
            player.move(0, 1, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_LEFT:
            player.move(0, -1, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_UP:
            player.move(-1, 0, grid, beat)
            collision = CollisionHandler(player, monster)
        if event.key == pygame.K_DOWN:
            player.move(1, 0, grid, beat)
            collision = CollisionHandler(player, monster)


class BeatHandler(object):
    '''
    This class checks whether the player follows the beat
    '''
    def __init__(self, loop_num, BEAT_CONST, MARGINAL_ERROR):
        """
        Precondition : 1) Loop_num (current frame number)
                       2) BEAT_CONST (predefined frames/beat constant)
                       3) Marginal Error (predefined allowed error of input)
        Postcondition : self.flag is True is following the beat within the
        marginal error, and False otherwise.
        """
        beat_rate = loop_num % BEAT_CONST
        if beat_rate < MARGINAL_ERROR or BEAT_CONST-beat_rate < MARGINAL_ERROR:
            self.flag = True
        else:
            self.flag = False


class CollisionHandler(object):
    '''This class checks if the player collides with a monster'''
    def __init__(self, player, monsters):
        """
        Precondition : Player object and Monster object
        Postcondition : self.flag = True if the location of each object
        overlaps, self.flag = False otherwise.
        """
        self.flag = False
        player_location = player.place
        # checks all the monster location to see if player is colliding with
        # one of the mosnters
        for monster_location in monsters.monsterlist:
            if player_location == monster_location and monsters.mode == 1:
                self.flag = True
                break

        # if two objects are colliding
        if (self.flag):
            player.decrease_energy()
