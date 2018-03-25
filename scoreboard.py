import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """show score info"""

    def __init__(self,ai_settings,screen,stats):
        """init score showed attribute"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #score font set
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #prepare init socre
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        

    def prep_ships(self):
        """show many ships left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 5 + ship_number * ship.rect.width;
            ship.rect.y = 5
            self.ships.add(ship)


    def prep_score(self):
        """switch score to img"""
        rounder_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounder_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #put score at screen right-top corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """swithch highest score to img"""
        high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)

        #put highest score at screen center
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx;
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """switch level info to img"""
        self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)

        #put level at score bottom
        self.level_rect       =  self.level_image.get_rect()
        self.level_rect.right =  self.score_rect.right
        self.level_rect.top   =  self.score_rect.bottom + 10


    def show_score(self):
        """show score at center"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)

        #draw ships
        self.ships.draw(self.screen)

        
