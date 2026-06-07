import pygame
import settings
from states.menu_state import MenuState
from states.play_state import PlayState
from states.game_over_state import GameOverState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_state = MenuState(self.switch_state)

    def switch_state(self, state_name, **kwargs):
        if state_name == "MENU":
            self.current_state = MenuState(self.switch_state)
        elif state_name == "PLAY":
            self.current_state = PlayState(self.switch_state)
        elif state_name == "GAME_OVER":
            self.current_state = GameOverState(self.switch_state, kwargs.get("final_score", 0))

    def run(self):
        while self.running:
            self.handle_events()
            
            delta_time = self.clock.tick(settings.FPS) / 1000.0
            
            self.update(delta_time)
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # States handle their own input queries directly or via InputManager
        self.current_state.handle_input()

    def update(self, delta_time):
        self.current_state.update(delta_time)

    def draw(self):
        self.current_state.draw(self.screen)
        pygame.display.flip()
