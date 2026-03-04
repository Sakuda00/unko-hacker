# -*- coding:utf-8 -*-
import pygame
from pygame.locals import QUIT, KEYDOWN
import random

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

# Physics
GRAVITY = 1400.0
JUMP_SPEED = 560.0
LAND_SNAP = 8

# Allowed letters
LETTERS = [chr(c) for c in range(ord("a"), ord("z") + 1)]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PX, PY))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pos_y = float(self.rect.y)
        self.vy = 0.0

    def sync_rect(self):
        self.rect.y = int(self.pos_y)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, letter, vx):
        super().__init__()
        self.image = pygame.Surface((OBX, OBY))
        self.image.fill((0, 120, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.letter = letter
        self.vx = float(vx)
        self.pos_x = float(self.rect.x)

    def move(self, dt):
        self.pos_x -= self.vx * dt
        self.rect.x = int(self.pos_x)


class GameState:
    def __init__(self):
        self.can_jump = True


State = GameState()


def next_block(player):
    rightx = IX
    righty = player.rect.bottomright[1] - OBY
    letter = random.choice(LETTERS)
    vx = random.randint(2, 7) * 60
    return Block(rightx, righty, letter, vx)


def main():
    pygame.init()
    screen = pygame.display.set_mode((IX, IY), 0, 32)
    pygame.display.set_caption("Key Jump")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    player = Player(IX / 2 - PX / 2, IY - PY)
    now_block = next_block(player)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, now_block)

    reloading = False
    score = 0

    while True:
        dt = clock.tick(60) / 1000.0

        if reloading:
            if player.rect.y < LY:
                for v in all_sprites:
                    v.rect.y += 7
                    if isinstance(v, Player):
                        v.pos_y = float(v.rect.y)
                    if isinstance(v, Block):
                        v.pos_x = float(v.rect.x)
                screen.fill((255, 255, 255))
                all_sprites.draw(screen)
                pygame.display.update()
                continue
            else:
                reloading = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if State.can_jump:
                    pressed = event.unicode.lower()
                    if pressed == now_block.letter:
                        State.can_jump = False
                        player.vy = -JUMP_SPEED

        # Physics update
        prev_bottom = player.rect.bottom
        player.vy += GRAVITY * dt
        player.pos_y += player.vy * dt
        player.sync_rect()

        # Move block
        now_block.move(dt)

        # Collision checks
        if pygame.sprite.collide_rect(player, now_block):
            landing = player.vy >= 0 and prev_bottom <= now_block.rect.top + LAND_SNAP
            if landing:
                player.rect.bottom = now_block.rect.top
                player.pos_y = float(player.rect.y)
                player.vy = 0.0
                State.can_jump = True

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

        # Fell off screen
        if player.rect.top > IY:
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


if __name__ == "__main__":
    main()