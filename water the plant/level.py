import random
import pygame
from setup import *


levels = {}
k = 0.04
for level in range(0, 1000+1):
    levels[level] = int((level**2) / (k))


class Level(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super().__init__()
        self.image = pygame.image.load("assets/star.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(topleft=(5,0))
        self.level = get_save("level")
        self.experience = get_save("experience")
        self.sprites = sprites

        self.update_level()

    def gain_experience(self):
        x, y = self.rect.bottomleft

        self.experience += random.randint(107, 209)
        save("experience", self.experience)
        self.set_level()
        self.update_level()
        
        if self.level > get_save("highest_level"):
            save("highest_level", self.level)
            fps = 8
            frames = loadGIF("assets/high_score.gif")
            high_score_sprite = MultiFrameSprite((0, 0), fps, frames)
            high_score_sprite.rect.topleft = (x+5, y+20)
            high_score_sprite.add(self.sprites)
            high_score_sprite.kill(delay=3)

    def set_level(self):
        if self.experience >= levels[self.level+1]:
            self.level += 1
            save("level", self.level)
        else:
            return
        return self.set_level()
    
    def update_level(self):
        self.image = pygame.image.load("assets/star.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.text_surface = font.render(str(self.level), 0, "white")
        width = self.text_surface.get_size()[0]
        self.image.blit(self.text_surface, (65-(width/2), 62))
