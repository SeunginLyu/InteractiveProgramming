import pygame
import numpy as np

WHITE = (255,255,255)
MAX_X = 3
MAX_Y = 3

class Grid:
    def __init__(self,x,y,width,height,color):
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Background:
    def __init__(self,name):
        self.pic = pygame.image.load(name)

class PygameKeyboardController:
    def __init__(self,model):
        self.model = model

    def handle_key_event(self,evemt):
        if event.type != pygame.keydown:
            return
        if event.type == pygame.K_LEFT:
            self.model.paddle.x += -10

class Player:
    def __init__(self,name,place):
        self.pic = pygame.image.load(name)
        self.pic = pygame.transform.rotozoom(self.pic,0,0.8)
        self.place = (place[0],place[1])

        self.flipped = False

    def move(self,dx,dy):
        x = self.place[0]+dx
        y = self.place[1]+dy
        if (dx == 1 or dy == 1) and not self.flipped:
            self.pic = pygame.transform.flip(self.pic,True,False)
            self.flipped = True
        if (dx == -1 or dy == -1) and self.flipped:
            self.pic = pygame.transform.flip(self.pic,True,False)
            self.flipped = False
        #if x<0 or x>MAX_X or y<0 or y>MAX_Y:
        #    x = 0
        #    y = 0
        self.place = (x,y)

    def get_absolute_location(self,canvas_size):
        absolute_x = (self.place[0]+1)*canvas_size[0]*1/50
        absolute_y = (self.place[1]+1)*canvas_size[1]*1/50
        return (absolute_x,absolute_y)

def main():
    pygame.init()
    pygame.display.set_caption('Artist')
    bg = Background('square.jpg')
    player = Player('player.png',(0,0))
    canvas_size = bg.pic.get_rect().size
    screen = pygame.display.set_mode(canvas_size)
    clock = pygame.time.Clock()
    done = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.move(1,0)
                if event.key == pygame.K_LEFT:
                    player.move(-1,0)
                if event.key == pygame.K_UP:
                    player.move(0,-1)
                if event.key == pygame.K_DOWN:
                    player.move(0,1)
        screen.blit(bg.pic,(0,0))
        screen.blit(player.pic,player.get_absolute_location(canvas_size))
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
