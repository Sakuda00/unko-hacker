import sys
import pygame
from pygame.locals import *

class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, alpha = 0):
        super().__init__()
        self.image = pygame.Surface((10, 50 + 50*alpha))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        print("THIS IS RECT", self.image.get_rect())
        self.rect.topleft = (x, y)
    def update(self, dy):
        self.rect.y += dy
        if (self.rect.y < 10):
            self.rect.y = 10
        elif self.rect.y > 420:
            self.rect.y = 420
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA) #20x20のグリッドを作ってる　多分透明 SRCALPHA
        pygame.draw.circle(self.image, (255, 255, 255), (10, 10), 10) #(10, 10) を中心とした半径10の円　グリッド内で
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vx = vx
        self.vy = vy
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.y <= 10 or self.rect.y >= 457.5):
            self.vy -= self.vy
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption("PONG")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    score1, score2 = 0, 0
    game_level = 2
    ball_speed = 5

    bar1 = Bar(10, 215)
    bar2 = Bar(620, 215, game_level * 0.2)
    ball = Ball(320, 240, ball_speed + game_level, ball_speed + game_level)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(bar1, bar2, ball)

    bar1_dy = 0
    running = True

    while running:
        for event in pygame.event.get():
            if (event.type == QUIT):
                running = False
            if (event.type == KEYDOWN):
                if (event.key == K_UP):
                    bar1_dy  =  -10
                elif event.key == K_DOWN:
                    bar1_dy = 10
            if event.type == KEYUP:
                if (event.key in (K_UP, K_DOWN)):
                    bar1_dy = 0
        bar1.update(bar1_dy)
        bar2.update((ball.rect.y - bar2.rect.y) * 0.1 * game_level)
        ball.update()


        if pygame.sprite.collide_rect(ball, bar1) or pygame.sprite.collide_rect(ball, bar2):
            ball.vx = -ball.vx
        
        if ball.rect.x < 5:
            score2 += 1
            ball.rect.center = (320, 240)
            ball.vx = 2
            ball.vy = 2
        elif ball.rect.x > 620:
            score1 += 1
            ball.rect.center = (320, 240)
            ball.vx = -2
            ball.vy = -2
        

        screen.fill((0, 50, 0))
        pygame.draw.aaline(screen, (255, 255, 255), (330, 5), (330, 475))

        all_sprites.draw(screen)
        screen.blit(font.render(str(score1), True, (255, 255, 255)), (255, 10))
        screen.blit(font.render(str(score2), True, (255, 255, 255)), (400, 10))
        pygame.display.update()
       # clock.tick(30)
if __name__ == "__main__":
    main()
        
