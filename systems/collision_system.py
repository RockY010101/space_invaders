import settings

class CollisionSystem:
    def __init__(self, bullet_manager, enemy_grid, player, score_manager, particle_system, ufo, sound_manager):
        self.bullet_manager = bullet_manager
        self.enemy_grid = enemy_grid
        self.player = player
        self.score_manager = score_manager
        self.particle_system = particle_system
        self.ufo = ufo
        self.sound_manager = sound_manager
        
    def check_all(self):
        # Player Bullet vs Enemies
        for bullet in self.bullet_manager.bullets:
            if not bullet.is_active or bullet.owner_tag != "player":
                continue
                
            for row in self.enemy_grid.grid:
                hit_found = False
                for enemy in row:
                    if enemy.is_alive and bullet.rect.colliderect(enemy.rect):
                        bullet.is_active = False
                        enemy.is_alive = False
                        self.enemy_grid.alive_count -= 1
                        self.score_manager.add_score(enemy.points)
                        self.particle_system.spawn_explosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2, enemy.color)
                        self.sound_manager.play("explosion")
                        hit_found = True
                        break
                if hit_found:
                    break
                    
            if not bullet.is_active:
                continue
                
            # Player Bullet vs UFO
            if self.ufo.is_active and bullet.rect.colliderect(self.ufo.rect):
                bullet.is_active = False
                points = self.ufo.get_points()
                self.score_manager.add_score(points)
                self.particle_system.spawn_explosion(self.ufo.x + self.ufo.width/2, self.ufo.y + self.ufo.height/2, settings.COLORS["RED"])
                self.sound_manager.play("explosion")
                self.ufo.despawn()

        # Enemy Bullet vs Player
        for bullet in self.bullet_manager.bullets:
            if not bullet.is_active or bullet.owner_tag != "enemy":
                continue
                
            if self.player.is_alive and bullet.rect.colliderect(self.player.rect):
                bullet.is_active = False
                self.particle_system.spawn_explosion(self.player.x + self.player.width/2, self.player.y + self.player.height/2, settings.COLORS["GREEN"], count=40)
                self.sound_manager.play("explosion")
                self.player.on_hit()
                is_game_over = self.score_manager.lose_life()
                if is_game_over:
                    return True

        # Enemy Body vs Player y-level
        for row in self.enemy_grid.grid:
            for enemy in row:
                if enemy.is_alive and enemy.y + enemy.height >= self.player.y:
                    return True
                    
        return False
