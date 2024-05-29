import json
import threading
import pygame
from time import sleep
from typing import Any
from PIL import Image, ImageSequence

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 720


def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
    return frames


class MultiFrameSprite(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, fps: int, list_of_frames: list, *, loop: bool=True, linger: int=0):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        if linger > 0:
            for _ in range(linger):
                list_of_frames.insert(0, list_of_frames[0])
        for frame in list_of_frames:
            self.frames.append(frame.convert_alpha())

        self.image = self.frames[0]
        self.rect  = self.image.get_rect()
        self.loop = loop

        self.millisec_rate = 1000 // fps
        self.current_frame = 0
        self.last_frame_at = 0
        self.rect.center = pos

    def update(self):
        time_now = pygame.time.get_ticks()
        if time_now > self.last_frame_at + self.millisec_rate:
            self.last_frame_at = time_now
            x,y = self.rect.center
            # print(self.current_frame != len(self.frames))
            if self.loop or self.current_frame != len(self.frames)-1:
                self.current_frame += 1
            if self.current_frame == len(self.frames) and self.loop:
                self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.rect  = self.image.get_rect()
            self.rect.center = (x,y)

    def kill(self, delay: float=0):
        delay_foo = threading.Thread(target=self.delayed_kill, args=[delay])
        delay_foo.start()

    def delayed_kill(self, delay: float=0):
        sleep(delay)
        pygame.sprite.Sprite.kill(self)


def clamp(value: int, max: int, min: int=0) -> int:
    if value > max:
        return max
    elif value < min:
        return min
    return value


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


pygame.font.init()
font = pygame.font.Font("assets/PublicPixel-E447g.ttf", 24)


def get_save(key: str=None) -> Any:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if key is None:
        return data
    else:
        return data.get(key)
    

def save(key: str, value: Any) -> None:
    data = get_save()
    data[key] = value
    with open("data.json", "w+") as f:
        json.dump(data, f)