import sys
import time
import pygame
from plant import Plant
from water import WateringCan
from level import Level, levels
from setup import *


class Restart(pygame.sprite.Sprite):
    def __init__(self, midbottom, game):
        super().__init__()
        self.image = pygame.image.load("assets/restart_button.png")
        self.rect = self.image.get_rect(midtop=midbottom)
        self.hover = pygame.image.load("assets/restart_button_hover.png")
        self.game = game
        self.pressed = False
        self.time = 0
    
    def update(self):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if hit:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.hover
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.pressed = True
                    self.time = time.time()
            fps = 12
            frames = loadGIF("assets/restart_button_pressed.gif")
            pressed = MultiFrameSprite(self.rect.center, fps, frames, loop=False)
            self.game.all_sprites.add(pressed)
            if self.pressed and time.time() >= self.time+len(frames)//fps:
                self.restart()
                print("restarting")
        else:
            self.image = pygame.image.load("assets/restart_button.png")
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def restart(self):
        save("level", 0)
        save("experience", 0)
        self.game.__init__()

    
class Game:
    def __init__(self) -> None:
        pygame.init()
        self.plant = Plant()
        self.timer = 0
        self.last_time = time.time()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Water the Plant")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.level = Level(sprites=self.all_sprites)
        self.watering_can = WateringCan(self.all_sprites, self.plant, self.level)
        self.all_sprites.add(self.level)
        self.all_sprites.add(self.plant)
        self.all_sprites.add(self.watering_can)

    def run(self):
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                self.screen.fill("light blue")
                if self.plant.dead:
                    background_image = pygame.image.load("assets/darken.png")
                    self.screen.blit(background_image, [0,0,WINDOW_WIDTH,WINDOW_HEIGHT])
                    if self.plant.dead != "checked":
                        deaths = get_save("deaths")
                        save("deaths", deaths+1)
                        self.death_text = Sprite((0, WINDOW_HEIGHT//2-200), "assets/death_text.png")
                        self.all_sprites.add(self.death_text)
                        restart_button = Restart(self.death_text.rect.midbottom, self)
                        self.all_sprites.add(restart_button)
                        self.plant.dead = "checked"
                else:
                    if not self.watering_can.watering:
                        self.timer += time.time() - self.last_time
                        self.last_time = time.time()
                        if self.timer >= 15*60:
                            self.timer = 0
                            self.plant.update_state(1)
                    

                x, y = self.level.rect.bottomleft
                max_width = self.level.image.get_size()[0] + 5
                pygame.draw.rect(self.screen, "white", [x+5,y+5, max_width,10], 5)
                percentage = (self.level.experience-levels[self.level.level])/(levels[self.level.level+1]-levels[self.level.level])
                pygame.draw.rect(self.screen, "green", [x+5,y+5, max_width*percentage,10], 10)    

                self.all_sprites.draw(self.screen)
                self.all_sprites.update()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()