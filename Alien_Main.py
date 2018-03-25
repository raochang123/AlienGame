import sys,os
import pygame
from settings import Settings
from ship import Ship
import game_func as gf
from gamestats import GameStats
from scoreboard import Scoreboard
from pygame.sprite import Group
from button import Button

highscore_filename ='\highscore.txt'

def run_game():
    pygame.init()
    #get highscore
    path = sys.path[0]
    path += highscore_filename
    print(path)
    high_score = gf.get_saved_highscore(path)
    bg_color =(230,230,230)
    ai_settings = Settings()
    stats  = GameStats(ai_settings)
    if len(high_score) == 2:
        stats.high_score = high_score[0]
        stats.level      = high_score[1]
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    ship  = Ship(ai_settings,screen)
    aliens = Group()
    #create one bullet
    bullets = Group()
    play_button = Button(ai_settings,screen,"Play")
    sb = Scoreboard(ai_settings,screen,stats)
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #while
    cnt = 0
    while True:
        #event
        gf.check_events(ship,ai_settings,screen,bullets,aliens,stats,play_button,sb)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings,screen,ship,aliens,bullets,stats,sb)
            gf.update_aliens(ai_settings,aliens,ship,stats,screen,bullets,sb)
        else:
            if cnt < 3:
                cnt += 1
                print('game over!')

        # draw
        gf.update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb)

run_game()


                
