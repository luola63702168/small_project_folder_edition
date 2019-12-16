import random

import pygame


SEREEN_RECT=pygame.Rect(0,0,480,700)
FRAME_PER_SEC=60
CREATE_ENEMY_EVENT=pygame.USEREVENT
HERO_FIRE_EVENT=pygame.USEREVENT+1
class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''
    def __init__(self,image_name,speed=1):
        """
        :param image_name:图片路径及名字
        :param speed:经历移动速度
        """
        super().__init__()
        self.image=pygame.image.load(image_name)
        self.rect=self.image.get_rect()
        self.speed=speed

    def update(self, *args):
        self.rect.y+=self.speed


class Background(GameSprite):
    '''游戏背景精灵'''
    def __init__(self,is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y=-self.rect.height

    def update(self, *args):
        super().update()
        if self.rect.y>=SEREEN_RECT.height:
            self.rect.y=-self.rect.height


class Enemy(GameSprite):
    '''敌机精灵'''
    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed=random.randint(1,3)
        self.rect.bottom=0
        max_x=SEREEN_RECT.width-self.rect.width
        self.rect.x=random.randint(0,max_x)

    def update(self, *args):
        super().update()
        if self.rect.y >= SEREEN_RECT.height:
            self.kill()

    def __del__(self):
        pass

class Hero(GameSprite):
    '''英雄精灵'''
    def __init__(self):
        super().__init__("./images/me1.png",0)
        self.rect.centerx=SEREEN_RECT.centerx
        self.rect.bottom=SEREEN_RECT.bottom-120
        self.bullets=pygame.sprite.Group()

    def update(self, *args):
        self.rect.x+=self.speed
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.right>SEREEN_RECT.right:
            self.rect.right=SEREEN_RECT.right

    def fire(self):
        for i in (0,1,2):
            bullet=Bullet()
            bullet.rect.bottom=self.rect.y-i*20
            bullet.rect.centerx=self.rect.centerx
            self.bullets.add(bullet)

class Bullet(GameSprite):
    '''子弹精灵'''
    def __init__(self):
        super().__init__("./images/bullet1.png",-2)

    def update(self, *args):
        super().update()
        if self.rect.bottom<0:
            self.kill()

    def __del__(self):
        pass



































