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
    def __init__(self,name):
        self.pic = pygame.image.load(name)
        print (self.pic.get_rect().size)

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
    bg = Background('square.jpg')
    canvas_size = bg.pic.get_rect().size
    screen = pygame.display.set_mode(canvas_size)
    done = False
    while not done:

        for event in pygame.event.get():   # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True   # Flag that we are done so we exit this loop
        screen.blit(bg.pic,(0,0))

        player = Player('player.png',(canvas_size[0]*3/5,canvas_size[1]*3/5))
        screen.blit(player.pic,player.place)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
