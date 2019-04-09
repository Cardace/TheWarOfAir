# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *
import time


def key_control(hero_temp):
    #获取事件，比如按键等
    for event in pygame.event.get():

        #判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        #判断是否是按下了键
        elif event.type == KEYDOWN:
            #检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                hero_temp.move_left()
            #检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                hero_temp.move_right()
            #检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')


class Bullet(object):
    def __init__(self, screen_temp, x, y):
        self.x = x + 40
        self.y = y - 20
        self.screen = screen_temp
        self.image = pygame.image.load("./feiji/bullet.png")

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= 10


class HeroPlane(object):
    def __init__(self, screen_temp):
        self.x = 195
        self.y = 700
        self.screen = screen_temp
        self.image = pygame.image.load("./feiji/hero1.png")
        self.bullet_list = []  # 存储发射出去的子弹的引用

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()

    # 当一直按下键盘时调用移动函数
    def press_move(self):
        if len(self.key_down_list) != 0:
            if self.key_down_list[0] == K_LEFT:
                self.move_left()
            elif self.key_down_list[0] == K_RIGHT:
                self.move_right()

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))


class EnemyPlane(object):
    """敌机的类"""

    def __init__(self, screen_temp):
        self.x = 0
        self.y = 0
        self.screen = screen_temp
        self.image = pygame.image.load("./feiji/enemy0.png")
        # self.bullet_list = [] #存储发射出去的子弹的引用
        self.direction = "right"  # 飞机默认移动方向

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

        # for bullet in self.bullet_list:
        #    bullet.display()
        #    bullet.move()

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        if self.x > 430:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))


def main():
    # 1. 创建窗口
    screen = pygame.display.set_mode((480, 852), 0, 32)

    # 2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")

    # 3. 创建一个飞机对象
    hero = HeroPlane(screen)

    # 4. 创建一个敌机对象
    enemy = EnemyPlane(screen)

    while True:
        screen.blit(background, (0, 0))

        hero.display()
        enemy.display()
        enemy.move()  # 调用敌机移动
        pygame.display.update()
        key_control(hero)

        time.sleep(0.01)


if __name__ == "__main__":
    main()
