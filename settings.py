class Settings():
    def __init__(self):

        #init set
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255,255,255)
        self.ship_speed_factor = 1.5
        self.ship_limit = 2
        #子弹设置
        self.bullet_speed_factor  = 3
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60,60,60,60
        self.bullet_allows = 20

        #alien setting
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed   = 10
        self.fleet_direction    = 1

        #recoed score
        self.alien_points = 50
        #game speed scale
        self.speedup_scale = 1.1
        #aliens score scale
        self.score_scale = 1.5


    def increase_speed(self):
        """increase speed and score_scale """
        if self.alien_points <= 1000:
            self.ship_speed_factor   *= self.speedup_scale
            self.bullet_speed_factor *= self.speedup_scale
            self.alien_speed_factor  *= self.speedup_scale

            self.alien_points =  int(self.alien_points * self.score_scale)
        
        
