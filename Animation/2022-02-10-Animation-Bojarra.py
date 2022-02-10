from ast import Break
import pygame
from pygame.constants import (QUIT, K_SPACE, K_d, K_e, K_w, K_ESCAPE, KEYDOWN)
import os



class Settings(object):
    window = {'width':300, 'height':200}
    fps = 60
    title = "Animation"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    directions = {'stop':(0, 0), 'down':(0,  1), 'up':(0, -1), 'left':(-1, 0), 'right':(1, 0)}

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

class Ryu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        for i in range(4):
            bitmap = pygame.image.load(Settings.imagepath(f"Ryu{i}.png")).convert()
            self.images.append(bitmap)
        self.imageindex = 0
        self.image = self.images[self.imageindex]
        self.rect = self.image.get_rect()
        self.rect.center = (Settings.window['width'] // 2, Settings.window['height'] // 2)
        self.animation_time = Timer(100)
        self.walking = False

    def jump(self):
        for i in range(6):
            bitmap = pygame.image.load(Settings.imagepath(f"Jump{i}.png")).convert_alpha()
            self.images.append(bitmap)
    
    def walk(self):
        for i in range(5):
            bitmap = pygame.image.load(Settings.imagepath(f"Walk{i}.png")).convert_alpha()
            self.images.append(bitmap)

    def hadouken (self):
        for i in range(5):
            bitmap = pygame.image.load(Settings.imagepath(f"Hadouken{i}.png")).convert_alpha()
            self.images.append(bitmap)

    def hitup (self):
        for i in range(5):
            bitmap = pygame.image.load(Settings.imagepath(f"HitUp{i}.png")).convert_alpha()
            self.images.append(bitmap)

    def update(self):
        if self.animation_time.is_next_stop_reached():
            self.imageindex += 1
            if self.imageindex >= len(self.images):
                self.imageindex = 0
            self.image = self.images[self.imageindex]


class RyuAnimation(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.ryu = pygame.sprite.GroupSingle(Ryu())
        self.running = False

    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.ryu.sprite.jump()
                elif event.key == K_d:
                    self.ryu.sprite.walk()
                elif event.key == K_e:
                    self.ryu.sprite.hadouken()
                elif event.key == K_w:
                    self.ryu.sprite.hitup()

    def update(self) -> None:
        self.ryu.update()

    def draw(self) -> None:
        self.screen.fill((200, 200, 200))
        self.ryu.draw(self.screen)
        pygame.display.flip()



if __name__ == '__main__':
    anim = RyuAnimation()
    anim.run()

