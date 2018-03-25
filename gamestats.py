class GameStats():
    """record game info"""
    def __init__(self,ai_settings):
        """init info"""
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score  = 0
        self.reset_stats()

    def reset_stats(self):
        #reset info
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        
