from entities.bullet import Bullet
import settings

class BulletManager:
    def __init__(self):
        self.bullets = []

    def update(self, delta_time):
        for bullet in self.bullets:
            bullet.update(delta_time)
            
        # Clean up inactive bullets
        self.bullets = [b for b in self.bullets if b.is_active]

    def draw(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def spawn_player_bullet(self, x, y):
        # Count current player bullets
        player_bullets = sum(1 for b in self.bullets if b.owner_tag == "player")
        
        if player_bullets < settings.MAX_PLAYER_BULLETS:
            new_bullet = Bullet(x, y, -settings.PLAYER_BULLET_SPEED, "player")
            self.bullets.append(new_bullet)
            return True
        return False

    def spawn_enemy_bullet(self, x, y):
        enemy_bullets = sum(1 for b in self.bullets if b.owner_tag == "enemy")
        if enemy_bullets < settings.MAX_ENEMY_BULLETS:
            new_bullet = Bullet(x, y, settings.ENEMY_BULLET_SPEED, "enemy")
            self.bullets.append(new_bullet)
            return True
        return False
