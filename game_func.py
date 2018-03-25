import sys,os
import pygame
from bullet import Bullet
from alien  import Alien
from time   import sleep

highscore_filename ='\highscore.txt'

def get_num_aliens_x(ai_settings,alien_width):
    """calc many aliens one line"""
    available_space_x = ai_settings.screen_width - 2*alien_width
    num_aliens_x = int(available_space_x / (2*alien_width))
    return num_aliens_x


def get_num_row(ai_settings,ship_height,alien_height):

    """calc many rows avaliable"""
    available_space_y = (ai_settings.screen_height -  2 * alien_height - ship_height)
    num_row = int(available_space_y /(2*alien_height))

    return num_row


def create_alien(ai_settings,screen,aliens,alien_num,row_number):
    """create one alien add into current line"""
    alien = Alien(ai_settings,screen)
    alien_width  = alien.rect.width
    alien.x = alien_width + 2 * alien_width*alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
    """create alien group"""
    """calc alien num"""
    """distance ,alien width"""
    alien = Alien(ai_settings,screen)
    num_alien_x = get_num_aliens_x(ai_settings,alien.rect.width)
    num_alien_y = get_num_row(ai_settings,ship.rect.height,alien.rect.height)

    #print("row:%d,col:%d" % (num_alien_x,num_alien_y))
    #create first line alien
    for row_num in range(num_alien_y):
        for alien_number in range(num_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_num)


def check_fleet_edges(ai_settings,aliens):
    """deal when aliens arrive at edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direct(ai_settings,aliens)
            break

def change_fleet_direct(ai_settings,aliens):
    """drop down aliens,change direct"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_alien_group_bottom_edge(screen,aliens):
    screen_rect = screen.get_rect()
    for alien in (aliens):
        if alien.rect.y >= screen_rect.bottom:
            #print("alien.rect.y:%d,screen bottom:%d",alien.rect.y,screen_rect.bottom)
            return True
        
    return False  
    
def update_aliens(ai_settings,aliens,ship,stats,screen,bullets,sb):
    """update alien pos"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #check alien and ship hit /*if hit ,return the alien*/
    if check_alien_group_bottom_edge(screen,aliens) or pygame.sprite.spritecollideany(ship,aliens): 
        print("Ship hit!!")
        sb.stats.score = 0
        sb.prep_score()
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
        sb.prep_ships()


def update_bullets(ai_settings,screen,ship,aliens,bullets,stats,sb):
    """refresh bullet pos ,remove invisible bullet"""
    for bullet_i in  bullets.copy():
        if bullet_i.rect.bottom < 0:
            bullets.remove(bullet_i)
    check_bullet_alien_collisons(ai_settings,screen,ship,aliens,bullets,stats,sb)

def check_high_score(stats,sb):
    """check get new highest score """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_collisons(ai_settings,screen,ship,aliens,bullets,stats,sb):
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
        
    if len(aliens) == 0:
        #remove all bullets, create new alien group
        ai_settings.increase_speed();
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)


def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    #response hit
    #
    if stats.ships_left >0:   
        stats.ships_left -= 1
        #clear alien and ship
        bullets.empty()
        aliens.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #
        sleep(2)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False

    
def check_keydown_events(event,ship,ai_settings,screen,bullets):
    """"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
   # elif event.key == pygame.K_UP or event.key == pygame.K_w:
    #    ship.moving_up = True
   # elif event.key == pygame.K_DOWN  or event.key == pygame.K_s:
    #    ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) <  ai_settings.bullet_allows:
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)

def check_keyup_events(event, ship,ai_settings,screen,bullets):
    """"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_down = False

def check_events(ship,ai_settings,screen,bullets,aliens,stats,play_button,sb):

    #event handle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            path = sys.path[0]
            path += highscore_filename
            save_highscore(stats.high_score,stats.level,path)
            os._exit(0)
        elif event.type == pygame.KEYDOWN:
            #print ('key down' + ' ' + str(event.key))
            check_keydown_events(event,ship,ai_settings,screen,bullets)
        elif event.type == pygame.KEYUP:
            #print ('key up')
            check_keyup_events(event, ship,ai_settings,screen,bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb)

def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb):
    """start new game when click the 'play' btn"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #hide cursor
        pygame.mouse.set_visible(False)
        stats.game_active = True
        stats.reset_stats()

        #reset score image
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #clear alien list and bullet list
        aliens.empty()
        bullets.empty()
        #create new aliens , center ship
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship() 

def update_screen(ai_settings,screen,ship,aliens,bullets,stats,play_button,sb):

    #draw
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def save_highscore(score,level,path):
    with open(path,'w+') as file:
        file.write(str(score)+'\n' + str(level))
        file.close()
        
def get_saved_highscore(path):
    score  = 0
    level  = 0
    nLine  = 0
    with open(path,'r+') as file:
        while True:
            lines = file.readline()
            if not lines:
               print('read error')
               break
            if nLine == 0:
                score = int(lines)
                print(score)
            elif nLine == 1:
                level = int(lines)
                print(level)
            nLine+= 1
        
        file.close()
        
    return (score,level)
