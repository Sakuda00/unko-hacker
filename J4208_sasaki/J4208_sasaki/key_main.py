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

# Spawn timing
MIN_SPAWN_TIME = 0.6
MAX_SPAWN_TIME = 1.4

# Allowed letters
LETTERS = [chr(c) for c in range(ord("a"), ord("z") + 1)]

# Block types
ENEMY = "enemy"      # red
BANANA = "banana"    # blue
FEMALE = "female"    # green
HUMAN = "human"      # yellow

TYPE_COLORS = {
    ENEMY: (220, 60, 60),
    BANANA: (60, 120, 255),
    FEMALE: (60, 200, 90),
    HUMAN: (240, 210, 60)
}


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PX, PY))
        self.image.fill((80, 80, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pos_y = float(self.rect.y)
        self.vy = 0.0

    def sync_rect(self):
        self.rect.y = int(self.pos_y)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, letter, vx, block_type):
        super().__init__()
        self.image = pygame.Surface((OBX, OBY))
        self.image.fill(TYPE_COLORS[block_type])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.letter = letter
        self.vx = float(vx)
        self.pos_x = float(self.rect.x)
        self.block_type = block_type

    def move(self, dt):
        self.pos_x -= self.vx * dt
        self.rect.x = int(self.pos_x)


class GameState:
    def __init__(self):
        self.can_jump = True
        self.banana = 0
        self.female = 0
        self.human = 0


State = GameState()


def next_block(player):
    rightx = IX
    righty = player.rect.bottomright[1] - OBY
    letter = random.choice(LETTERS)
    vx = random.randint(2, 7) * 60
    block_type = random.choice([ENEMY, BANANA, FEMALE, HUMAN])
    return Block(rightx, righty, letter, vx, block_type)


def draw_gauges(screen, font):
    banana_text = font.render(f"BANANA: {State.banana}", True, (0, 0, 0))
    female_text = font.render(f"GIRLS: {State.female}", True, (0, 0, 0))
    human_text = font.render(f"HUMAN: {State.human}", True, (0, 0, 0))
    screen.blit(banana_text, (10, 10))
    screen.blit(female_text, (10, 40))
    screen.blit(human_text, (10, 70))


def main():
    pygame.init()
    screen = pygame.display.set_mode((IX, IY), 0, 32)
    pygame.display.set_caption("Gorilla Escape")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    player = Player(IX / 2 - PX / 2, IY - PY)
    blocks = pygame.sprite.Group()

    blocks.add(next_block(player))

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    reloading = False
    spawn_timer = 0.0
    spawn_interval = random.uniform(MIN_SPAWN_TIME, MAX_SPAWN_TIME)

    while True:
        dt = clock.tick(60) / 1000.0
        spawn_timer += dt

        if spawn_timer >= spawn_interval:
            new_block = next_block(player)
            blocks.add(new_block)
            spawn_timer = 0.0
            spawn_interval = random.uniform(MIN_SPAWN_TIME, MAX_SPAWN_TIME)

        if reloading:
            if player.rect.y < LY:
                for v in all_sprites:
                    v.rect.y += 7
                    if isinstance(v, Player):
                        v.pos_y = float(v.rect.y)
                for b in blocks:
                    b.rect.y += 7
                    b.pos_x = float(b.rect.x)
                screen.fill((255, 255, 255))
                all_sprites.draw(screen)
                blocks.draw(screen)
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
                    # jump only with current block key (closest to player)
                    nearest = min(blocks, key=lambda b: abs(b.rect.centerx - player.rect.centerx))
                    if pressed == nearest.letter:
                        State.can_jump = False
                        player.vy = -JUMP_SPEED

        # Physics update
        prev_bottom = player.rect.bottom
        player.vy += GRAVITY * dt
        player.pos_y += player.vy * dt
        player.sync_rect()

        # Move blocks
        for block in list(blocks):
            block.move(dt)
            if block.rect.right < 0:
                blocks.remove(block)

        # Collision checks
        for block in list(blocks):
            if pygame.sprite.collide_rect(player, block):
                landing = player.vy >= 0 and prev_bottom <= block.rect.top + LAND_SNAP
                if block.block_type == ENEMY:
                    if State.human > 0:
                        State.human -= 1
                        blocks.remove(block)
                    else:
                        print("Game Over (enemy)")
                        return

                elif block.block_type == BANANA:
                    if not State.can_jump and landing:
                        # if jumping, don't count banana
                        pass
                    if State.can_jump and landing:
                        State.banana += 1
                        blocks.remove(block)
                        player.rect.bottom = block.rect.top
                        player.pos_y = float(player.rect.y)
                        player.vy = 0.0

                elif block.block_type == FEMALE:
                    if landing and pygame.key.get_pressed()[pygame.key.key_code(block.letter)]:
                        State.female += 1
                        blocks.remove(block)
                    elif landing:
                        # landing on female gorilla is game over
                        print("Game Over (female landing)")
                        return

                elif block.block_type == HUMAN:
                    if State.can_jump and landing:
                        State.human += 1
                        blocks.remove(block)
                        player.rect.bottom = block.rect.top
                        player.pos_y = float(player.rect.y)
                        player.vy = 0.0

                if landing and block.block_type in (BANANA, HUMAN):
                    State.can_jump = True

        # Missed landing
        for block in blocks:
            if block.rect.right < player.rect.left and block.block_type == ENEMY:
                print("Game Over (missed enemy)")
                return

        # Fell off screen
        if player.rect.top > IY:
            print("Game Over")
            return

        screen.fill((255, 255, 255))
        blocks.draw(screen)
        all_sprites.draw(screen)

        for block in blocks:
            letter_surface = font.render(block.letter, True, (255, 255, 255))
            letter_rect = letter_surface.get_rect(center=block.rect.center)
            screen.blit(letter_surface, letter_rect)

        draw_gauges(screen, font)

        pygame.display.update()


if __name__ == "__main__":
    main()