import time
import asyncio
import pygame
from setup import *


cooldown = 20*60


class WateringCan(pygame.sprite.Sprite):
    def __init__(self, sprites, plant, level):
        super().__init__()
        self.image = pygame.image.load("assets/watering_can.png")
        self.rect = self.image.get_rect(topright=(WINDOW_WIDTH-10, -40))
        self.watering = False
        self.sprites = sprites
        self.plant = plant
        self.level = level
        self.animation_timer = 0
        self.cooldown_time = 0 if self.level == 0 else time.time()

    def update(self):
        if self.plant.dead: return
        
        width, height = self.image.get_size()

        self.cooldown = time.time() - self.cooldown_time
        if self.cooldown < cooldown:
            self.image = pygame.image.load("assets/watering_can.png")
            percentage = 1-(cooldown - self.cooldown) / (cooldown)
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 0))
            pygame.draw.rect(overlay, (0, 0, 0, 100), [0, height*percentage, width+3, height])
            self.image.blit(overlay, [0, 0, width, height])
            seconds_raw = cooldown-self.cooldown
            minutes = seconds_raw//60
            seconds = seconds_raw%60
            text = (f"{minutes:.0f}m" if minutes != 0 else "") + (f" {seconds:.1f}s" if seconds != 0 else "")
            text_surface = font.render(text, 0, "white")
            ts_width, ts_height = text_surface.get_size()
            self.image.blit(text_surface, (width//2-ts_width//2, height//2-ts_height//2))
            return

        if self.watering:
            self.animation_timer += time.time() - self.last_time
            self.last_time = time.time()
            if self.animation_timer >= 3.3:
                self.animation_timer = 0
                self.count += 1
                self.plant.update_state(-1)
            if self.count == 3:
                self.watering = False
                self.watering_sprite.kill()
                self.level.gain_experience()
                self.cooldown = cooldown
                self.cooldown_time = time.time()
            return
        
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if hit:
            pygame.draw.rect(self.image, (255, 255, 255, 100), [0, 0, width+3, height-5])
            self.image.blit(pygame.image.load("assets/watering_can.png"), [0, 0, width, height])
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.water()
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            self.image = pygame.image.load("assets/watering_can.png")
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def water(self):
        self.watering = True
        self.image = pygame.image.load("assets/watering_can_tilted.png")
        self.watering_sprite = MultiFrameSprite((100, 100), 10, loadGIF("assets/watering.gif"), loop=True, linger=2)
        self.watering_sprite.rect.topright = self.rect.bottomleft
        self.watering_sprite.rect.y -= 100
        self.watering_sprite.rect.x += 100
        self.sprites.add(self.watering_sprite)
        self.last_time = time.time()
        self.count = 0


