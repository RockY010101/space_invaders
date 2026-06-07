from entities.enemy import Enemy
import settings
import random

class EnemyGrid:
    def __init__(self):
        self.grid = []
        self.direction = 1 # 1 for right, -1 for left
        self.level = 1
        self.move_timer = settings.BASE_MOVE_INTERVAL
        self.move_interval = settings.BASE_MOVE_INTERVAL
        
        self.shoot_interval = settings.BASE_SHOOT_INTERVAL
        self.shoot_timer = random.uniform(0.5, self.shoot_interval)
        
        # Build grid
        for row in range(settings.ENEMY_ROWS):
            grid_row = []
            for col in range(settings.ENEMY_COLS):
                x = settings.GRID_START_X + col * settings.ENEMY_SPACING_X
                y = settings.GRID_START_Y + row * settings.ENEMY_SPACING_Y
                # Alternate enemy types horizontally
                enemy_type = 1 if col % 2 == 0 else 2
                enemy = Enemy(row, col, x, y, enemy_type)
                grid_row.append(enemy)
            self.grid.append(grid_row)
            
        self.alive_count = settings.ENEMY_ROWS * settings.ENEMY_COLS
        self.total_count = self.alive_count
        
    def reset(self, level=1):
        self.grid = []
        self.direction = 1
        self.level = level
        
        # Increase speed slightly based on level
        speed_multiplier = max(0.2, 1.0 - (level - 1) * 0.1)
        self.move_interval = settings.BASE_MOVE_INTERVAL * speed_multiplier
        self.move_timer = self.move_interval
        
        self.shoot_timer = random.uniform(0.5, self.shoot_interval)
        
        # Build grid
        for row in range(settings.ENEMY_ROWS):
            grid_row = []
            for col in range(settings.ENEMY_COLS):
                x = settings.GRID_START_X + col * settings.ENEMY_SPACING_X
                y = settings.GRID_START_Y + row * settings.ENEMY_SPACING_Y
                enemy_type = 1 if col % 2 == 0 else 2
                enemy = Enemy(row, col, x, y, enemy_type)
                grid_row.append(enemy)
            self.grid.append(grid_row)
            
        self.alive_count = settings.ENEMY_ROWS * settings.ENEMY_COLS
        self.total_count = self.alive_count

    def update(self, delta_time, bullet_manager):
        if self.alive_count == 0:
            return
            
        self.move_timer -= delta_time
        if self.move_timer <= 0:
            self._move_grid()
            # Speed up as enemies die
            ratio = max(0.1, self.alive_count / self.total_count)
            self.move_interval = settings.BASE_MOVE_INTERVAL * ratio
            self.move_timer = self.move_interval
            
        # Shoot logic
        self.shoot_timer -= delta_time
        if self.shoot_timer <= 0:
            self._try_shoot(bullet_manager)
            
            # Base interval
            interval = self.shoot_interval
            
            # If level > half of alive ships, increase fire rate by 5% per excess level
            threshold = max(1, self.alive_count // 2)
            if self.level > threshold:
                excess_levels = self.level - threshold
                multiplier = 0.95 ** excess_levels
                interval *= max(0.2, multiplier)
                
            self.shoot_timer = random.uniform(interval * 0.5, interval)
            
    def _try_shoot(self, bullet_manager):
        # Find columns that have at least one living enemy
        active_cols = []
        for col in range(settings.ENEMY_COLS):
            for row in range(settings.ENEMY_ROWS - 1, -1, -1):
                if self.grid[row][col].is_alive:
                    active_cols.append(col)
                    break
                    
        if not active_cols:
            return
            
        num_shots = min(self.level, max(1, self.alive_count // 2))
        num_shots = min(num_shots, len(active_cols))
        
        # Pick unique columns if possible
        chosen_cols = random.sample(active_cols, num_shots)
        
        for chosen_col in chosen_cols:
            # Find the lowest enemy in this column
            for row in range(settings.ENEMY_ROWS - 1, -1, -1):
                enemy = self.grid[row][chosen_col]
                if enemy.is_alive:
                    bullet_manager.spawn_enemy_bullet(enemy.x + enemy.width / 2, enemy.y + enemy.height)
                    break
            
    def _move_grid(self):
        hit_edge = False
        
        # Check edge
        for row in self.grid:
            for enemy in row:
                if enemy.is_alive:
                    next_x = enemy.x + (self.direction * settings.ENEMY_STEP_DISTANCE)
                    if next_x <= 0 or next_x + enemy.width >= settings.SCREEN_WIDTH:
                        hit_edge = True
                        break
            if hit_edge:
                break
                
        if hit_edge:
            self.direction *= -1
            dy = settings.ENEMY_DROP_DISTANCE + ((self.level - 1) * 2)
            dx = 0
        else:
            dy = 0
            dx = self.direction * settings.ENEMY_STEP_DISTANCE
            
        for row in self.grid:
            for enemy in row:
                if enemy.is_alive:
                    enemy.update_position(enemy.x + dx, enemy.y + dy)

    def draw(self, surface):
        for row in self.grid:
            for enemy in row:
                enemy.draw(surface)
