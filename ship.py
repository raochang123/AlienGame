import  pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        """init ship"""
        super(Ship,self).__init__()
        #init pos
        self.screen = screen
        self.ai_settings = ai_settings
        #load img and get rectangle area

        self.image = pygame.image.load('images/ship2.bmp')
        self.rect  = self.image.get_rect()
        self.screen_rect = screen.get_rect();

        # put each ship to screen bottom center pos
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left  = False
        self.moving_up    =  False
        self.moving_down  = False

        self.center = float(self.rect.centerx)


    def update(self):
        #adj pos
        if self.moving_right and  self.rect.right  < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left >0:
            self.rect.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top >0:
            self.rect.top -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom  < self.screen_rect.bottom:
             self.rect.bottom += self.ai_settings.ship_speed_factor
        
    def blitme(self):
        # draw ship
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
        
