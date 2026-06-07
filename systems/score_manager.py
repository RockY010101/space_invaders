class ScoreManager:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        
    def add_score(self, points):
        self.score += points
        
    def lose_life(self):
        self.lives -= 1
        return self.lives <= 0
        
    def reset(self):
        self.score = 0
        self.lives = 3
