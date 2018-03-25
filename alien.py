import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ single alien class"""

    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect  = self.image.get_rect()
        #print (self.rect.width)

        #alien pos
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #save alien pos
        self.x = float(self.rect.x)


    def update(self):
        """move alien to right"""
        self.x += (self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        """if alien at screen edge,return true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <=0:
            return True
        else:
            return False

        
    def blitme(self):
        """ draw alien """
        self.screen.blit(self.image,self.rect)

        
