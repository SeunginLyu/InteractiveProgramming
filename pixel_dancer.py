import pygame

WHITE = (255,255,255)

class Grid:
    def __init__(self,x,y,width,height,color):
        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Background:
    def __init__(self,name,place):
        self.pic = pygame.image.load(name)
        self.place = place

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
        self.place = place

    def move(self):
        pass

def main():
    pygame.init()
    pygame.display.set_caption('Artist')
    screen = pygame.display.set_mode([800,600])
    done = False
    while not done:

        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done so we exit this loop

        bg = Background('starry_night.jpg',(50,150))
        screen.blit(bg.pic,bg.place)

        player = Player('player.png',(50,300))
        screen.blit(player.pic,player.place)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
