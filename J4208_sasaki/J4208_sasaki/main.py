# -*- coding:utf-8 -*-
import sys
import pygame
from pygame.locals import *
import time
import random


PX = 90
PY = 167

OBX = 90
OBY = 90

LY = 200



IX = 500

IY = 700


LT = 0.15
LT1 = 0.30
LT2  = 0.78


BX = 45
BY = 90



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/endure_human2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def yupdate(self, y):
        self.rect.y = y


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, kind, vx):
        ##斜めいどうもあってもいいかも
        super().__init__()
        self.image = pygame.image.load("images/toilet.png").convert_alpha()
        if (kind == 0):
            None
            #self.image.fill((0, 255, 0))
        elif (kind == 1) :
            None
            #self.image.fill((0, 0, 255))
        self.dir = direction
        self.rect = self.image.get_rect()
        dd = 0
        if (direction > 0):

            dd = 0
            None
        else:
            dd  = (vx * 40)
        self.rect.topleft = (x   + dd, y)
        self.vx = vx
    def move(self):
        self.rect.x += self.dir * self.vx
    def delete(self):
        self.kill()
    


    
class BarierObject(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, kind, vx):
        ##斜めいどうもあってもいいかも
        super().__init__()
        ##self.image = pygame.image.load("images/toilet.png").convert_alpha()
        self.image = pygame.Surface((OBX, OBY))
        self.image.fill((0, 255, 0))
        self.dir = direction
        self.rect = self.image.get_rect()
        dd = 0
        if (direction > 0):
            dd = 0
            None
        else:
            dd  = (vx * 40)
        self.rect.topleft = (x   + dd, y)
        self.vx = vx
    def move(self):
        self.rect.x += self.dir * self.vx

    def delete(self):
        self.kill()
    


class Barier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        ##self.image = pygame.image.load("images/toilet.png").convert_alpha()
        self.image = pygame.Surface((BX, BY))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def delete(self):
        self.kill()

class Poop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/unkosample2.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

def score_eval(pl, pr, x, y):
    d = min(pr-  pl, y - x)
    covers = min(pr, y) - max(pl, x)
    if (covers <= 0):
        return -1
    s = covers / d
    s *= 100
    return s


#蛙？　蛙かげんしょうゲーム

class PlayerState:
    def __init__(self):
        self.jumping = False
        self.barier_comming = False
        self.left_barier = False
        self.right_barier = False
        Guard = False



State = PlayerState()


def Next_Obstacle(player, nowOB):
    global State
    rightx = 0
    righty = player.rect.bottomright[1] - OBY

    leftx = IX - OBX
    lefty = righty

    State.barier_comming = False

   
    VX = random.randint(2,4)
    KIND = random.randint(1, 2)
    DIR = random.randint(1, 2)
    X = -1
    Y = -1
    if (DIR == 1):
        X = rightx
        Y = righty
    else:
        X = leftx
        Y = lefty
        DIR = -1


    if (KIND == 2):
        State.barier_comming = True
        return BarierObject(X, Y, DIR, KIND, VX)
        
    

    return Obstacle(X, Y, DIR, KIND, VX)



def main():
    global State
    v0 =50
    g = 9.8

    # Pygameの初期設定
    pygame.init()
    screen = pygame.display.set_mode((IX, IY), 0, 32)
    pygame.display.set_caption("demo")
    clock = pygame.time.Clock()
    running = True
    

    player = Player(IX/2, IY - PY)
    Ob1 = Obstacle(0, IY - OBY, 1, 0, 1)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player, Ob1)
    isHit = False
    jumping = False
    st = -1
    sth = -1
    nowOb = Ob1
    score = 0
    reloading = False

    Add_Poop = False

    Poops = []


    Left_Barier = None
    Right_Barier = None


    while running:
        if (reloading):
            #RELOAD
            print("realodgin")
            if (player.rect.y < LY):
                for v in all_sprites:
                    v.rect.y += 7
                screen.fill((255, 255, 255))
                all_sprites.draw(screen)
                pygame.display.update()
                clock.tick(60)
                continue
            else:
                reloading = False
        
     #   print("NOWY ", player.rect.y)
      #  print("SCORE", score)
       # print("NOW ", nowOb.rect.x, nowOb.rect.y)
        for event in pygame.event.get():
            if(event.type == QUIT):
                running = False

            if (event.type == KEYDOWN):
                if (not jumping):
                    jumping = True
                    st = time.time()
                    sth = player.rect.y
                    
        

        if (jumping):
            t = time.time() - st
            t *= 10
            dh = (v0 * t) - (g * t * t * 0.5)
            if (( (t >= LT or t >= LT1)    or (t >= LT2) )and Add_Poop == False):
                New_Poop = Poop(player.rect.bottomleft[0] + random.randint(-70, 70), player.rect.bottomleft[1] - 40)
                all_sprites.add(New_Poop)
                Poops.append(New_Poop)
                print("ADPPO")
                if (t >= LT2):
                    Add_Poop = True
            if (dh < 0):
                jumping = False 
                Add_Poop = False
                print("FALS")
            else:
            
                nh = sth -  dh
                player.yupdate(nh)

        


        if (not State.barier_comming):
            IsGuard = False
            if (State.left_barier and pygame.sprite.collide_rect(Left_Barier, nowOb)):
                Left_Barier.kill()
                print("KILL LEFT")
                Left_Barier = None
                State.left_barier = False
                IsGuard = True
                
            if (State.right_barier and pygame.sprite.collide_rect(Right_Barier, nowOb)):
                Right_Barier.kill()
                print("KILL RIGHT")
                Right_Barier = None
                State.right_barier = False
                IsGuard = True
            if (IsGuard):
                Add_Poop = False
                jumping = False
                newOb = Next_Obstacle(player, nowOb)
                nowOb = newOb
                all_sprites.add(nowOb)
                print ("Summon new ob")

        if (Left_Barier != None and pygame.sprite.collide_rect(player, Left_Barier)):
            print("COLLIDE LEFT")

        if pygame.sprite.collide_rect(player, nowOb):
            print(player.rect.x, player.rect.y)
            print(nowOb.rect.bottomright,nowOb.rect.y)
            jumping = False
          #  print(player.rect.bottomright, "PL")
           # print(nowOb.rect.topright, "BO")
            if (abs(player.rect.bottomright[1] - nowOb.rect.topright[1]) <= 10):
                print("ABOVE")
                #newOb = Obstacle(0, player.rect.bottomright[1] - OBY, 1, 0, 2)
                newOb = Next_Obstacle(player, nowOb)
                getscore = score_eval(player.rect.x, player.rect.bottomright[0], nowOb.rect.x, nowOb.rect.bottomright[0])
                player.rect.y = nowOb.rect.topleft[1] - PY
                Add_Poop = False
                if (getscore == -1):
                    print("Game OVER RANGE OVER")
                    break
                score += getscore
                nowOb = newOb
                print ("NEW")
                all_sprites.add(nowOb)

                if (player.rect.y < LY):
                    print("KITA")
                    """"
                    dy = LY - player.rect.y
                    
                    for v in all_sprites:
                        v.rect.y += dy
                        print("NXTY ", v.rect.y)
                    print("NXTPLY", player.rect.y)
                    """
                    reloading = True
                    
                isHit = False  
                
            else:
                ##Barierとあたったか判定
                print(nowOb, player.rect.bottomleft, nowOb.rect.bottomleft, State.barier_comming)
                if (State.barier_comming):
                    dif = abs(player.rect.bottomleft[1] - nowOb.rect.bottomleft[1])
                    print("YE ", dif)
                    Add_Poop = False
                    if (not jumping):
                        if (not State.left_barier):
                            Left_Barier = Barier(player.rect.bottomleft[0] - BX, player.rect.bottomleft[1] - BY)
                            print(player.rect.bottomleft[0], "LFE")
                            all_sprites.add(Left_Barier)
                        if (not State.right_barier):
                            print(player.rect.bottomright[0], "RIGHT")
                            Right_Barier = Barier(player.rect.bottomright[0], player.rect.bottomright[1] - BY)
                            all_sprites.add(Right_Barier)
                        State.left_barier = True
                        State.right_barier = True
                    State.barier_comming  = False
                    nowOb.delete()
                    newOb = Next_Obstacle(player, nowOb)
                    nowOb = newOb
                    all_sprites.add(nowOb)
                    jumping = False
                    isHit = False
    
                else:
                    print("GAme over")
                    break
                print("SIDE")
        if (isHit == False):
            nowOb.move()
        #poop process
        for poop in Poops:
            if (poop.rect.y < 0):
                continue
            poop.update(random.randint(-2, 2), 3)

       # print("NOWW", nowOb.dir, nowOb.rect.x, player.rect.bottomright)
        if (nowOb.dir == 1 and nowOb.rect.x > player.rect.bottomright[0]):
            print("Game OVER")
            break
        if (nowOb.dir == -1 and nowOb.rect.bottomright[0] < player.rect.bottomleft[0]):
            print ("GAME OVER")
            break
            
        if (State.left_barier):
            Left_Barier.move(player.rect.bottomleft[0] - BX, player.rect.bottomleft[1] - BY)
        if (State.right_barier):
            Right_Barier.move(player.rect.bottomright[0], player.rect.bottomright[1] - BY)
        
        
        screen.fill((255, 255, 255))
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()


