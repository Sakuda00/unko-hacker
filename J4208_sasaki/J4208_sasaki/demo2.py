import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ブロックのサイズ
BLOCK_SIZE = 30

# ブロック用のSpriteクラス
class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - BLOCK_SIZE)
        self.rect.y = random.randint(0, HEIGHT - BLOCK_SIZE)

# Spriteグループを用意
blocks = pygame.sprite.Group()

# 新しいブロックを追加する関数
def add_block():
    block = Block()
    blocks.add(block)

# タイマー用の変数
ADD_BLOCK_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BLOCK_EVENT, 1000)  # 1秒ごとに新しいブロックを追加

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_BLOCK_EVENT:
            add_block()

    screen.fill((0, 0, 0))

    # すべてのブロックを描画
    blocks.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()