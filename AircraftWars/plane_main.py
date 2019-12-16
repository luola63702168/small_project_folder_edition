import pygame
from plane_sprites import *


class PlaneGame(object):
    '''飞机大战主游戏'''
    def __init__(self):
        print("游戏初始化")
        # 1-1.创建游戏窗口
        self.screen=pygame.display.set_mode(SEREEN_RECT.size)
        # 1-2 创建游戏的时钟
        self.clock=pygame.time.Clock()
        # 1-3 调用私有方法
        self.__create_sprites()
        # 4-1 设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)

        pygame.time.set_timer(HERO_FIRE_EVENT,500) 

    def __create_sprites(self):
        """
        3-1 创建背景精灵和精灵组
        """
        bg1 = Background()
        bg2 = Background(is_alt=True)
        self.back_group=pygame.sprite.Group(bg1,bg2)
        self.enemy_group=pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group=pygame.sprite.Group(self.hero)

    def start_game(self):
        print('游戏开始')
        while True:
            # 2-1 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2-2 事件监听
            self.__event_handler()
            # 2-3 碰撞检测
            self.__check_collide()
            # 2-4 更新/绘制精灵组
            self.__update_sprites()
            # 2-5 更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                PlaneGame.__game_over() 
            elif event.type==CREATE_ENEMY_EVENT:
                # print("敌机出场%s" % CREATE_ENEMY_EVENT)
                enemy=Enemy()
                self.enemy_group.add(enemy)
            elif event.type==HERO_FIRE_EVENT:
                self.hero.fire()
        keys_pressed=pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed=2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed=-2
        else:
            self.hero.speed=0


    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,True)
        enemies=pygame.sprite.spritecollide(self.hero,self.enemy_group,True)  
        if len(enemies)>0:
            self.hero.kill()
            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod 
    def __game_over():
        print("游戏结束")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 检查
    pygame.init()
    # 创建游戏对象
    game=PlaneGame()
    # 启动游戏
    game.start_game()





























