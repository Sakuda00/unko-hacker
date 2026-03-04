# -*- coding:utf-8 -*-
import pygame
from pygame.locals import QUIT, KEYDOWN
import random
import time

# Screen size
IX = 500
IY = 700

# Player size
PX = 60
PY = 90

# Block size
OBX = 90
OBY = 90

# Scroll threshold
LY = 200

# Jump physics
V0 = 50
G = 9.8

# Allowed letters
LETTERS = [chr(c) for c in range(ord("a"), ord("z") + 1)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PX, PY))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def yupdate(self, y):
        self.rect.y = y


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, letter, vx):
        super().__init__()
        self.image = pygame.Surface((OBX, OBY))
        self.image.fill((0, 120, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.letter = letter
        self.vx = vx

    def move(self):
        self.rect.x -= self.vx


class GameState:
    def __init__(self):
        self.jumping = False


State = GameState()


def next_block(player):
    rightx = IX
    righty = player.rect.bottomright[1] - OBY
    letter = random.choice(LETTERS)
    vx = random.randint(2, 7)
    return Block(rightx, righty, letter, vx)


def main():
    global State

    pygame.init()
    screen = pygame.display.set_mode((IX, IY), 0, 32)
    pygame.display.set_caption("Key Jump")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    player = Player(IX / 2 - PX / 2, IY - PY)
    now_block = next_block(player)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, now_block)

    jumping = False
    st = -1
    sth = -1
    reloading = False
    score = 0

    while True:
        if reloading:
            if player.rect.y < LY:
                for v in all_sprites:
                    v.rect.y += 7
                screen.fill((255, 255, 255))
                all_sprites.draw(screen)
                pygame.display.update()
                clock.tick(60)
                continue
            else:
                reloading = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if not jumping:
                    pressed = event.unicode.lower()
                    if pressed == now_block.letter:
                        jumping = True
                        st = time.time()
                        sth = player.rect.y

        if jumping:
            t = (time.time() - st) * 10
            dh = (V0 * t) - (G * t * t * 0.5)
            if dh < 0:
                jumping = False
            else:
                nh = sth - dh
                player.yupdate(nh)

        # Move block
        now_block.move()

        # Collision checks
        if pygame.sprite.collide_rect(player, now_block):
            # Landing from above
            if abs(player.rect.bottomright[1] - now_block.rect.topright[1]) <= 10:
                player.rect.y = now_block.rect.topleft[1] - PY
                score += 100
                now_block.kill()
                now_block = next_block(player)
                all_sprites.add(now_block)
                if player.rect.y < LY:
                    reloading = True
            else:
                print("Game Over")
                return

        # Missed landing (block passed player)
        if now_block.rect.right < player.rect.left:
            print("Game Over")
            return

        screen.fill((255, 255, 255))
        all_sprites.draw(screen)

        # Draw letter on block
        letter_surface = font.render(now_block.letter, True, (255, 255, 255))
        letter_rect = letter_surface.get_rect(center=now_block.rect.center)
        screen.blit(letter_surface, letter_rect)

        # Score
        score_surface = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()