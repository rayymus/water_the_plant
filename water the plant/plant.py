import pygame
from setup import *


class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/plant_dry_1.png")
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.rect.bottom = WINDOW_HEIGHT*1.12
        self.dry_state = 1 if get_save("level") == 0 else 0
        self.dead = False
        self.update_state(0)

    def update_state(self, amount: int):
        self.dry_state = clamp(self.dry_state+amount, 4, 0)
        save("dry_state", self.dry_state)
        if self.dry_state == 4:
            self.dead = True
            return
        if self.dry_state == 0:
            self.image = pygame.image.load("assets/plant.png")
        else:
            self.image = pygame.image.load(f"assets/plant_dry_{self.dry_state}.png")
        