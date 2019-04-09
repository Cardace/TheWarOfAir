import pygame
import time
import random
from pygame.locals import *


def key_control(hero_temp):
    #获取事件，比如按键等
    for event in pygame.event.get():

        #判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        #判断是否是按下了键
        elif event.type == KEYDOWN:
            #检测按键是否是left
            if event.key == K_LEFT:
                print('left')
                hero_temp.key_down(K_LEFT)
            #检测按键是否是right
            elif event.key == K_RIGHT:
                print('right')
                hero_temp.key_down(K_RIGHT)
            #检测按键是否是空格键
            elif event.key == K_SPACE:
                print('space')
                hero_temp.fire()
            elif event.key == K_b:#自爆
                print('b')
                hero_temp.bomb()
        #判断是否是松开了键
        elif event.type == KEYUP:
            #检测松键是否是left
            if event.key == K_LEFT:
                print('left')
                hero_temp.key_up(K_LEFT)
            #检测按键是否是right
            elif event.key == K_RIGHT:
                print('right')
                hero_temp.key_up(K_RIGHT)

class Base(object):
    """docstring for Base"""
    def __init__(self, screen_temp, x, y, image_name, picture_num):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
        #爆炸效果用的如下属性
        self.hit = False #表示是否要爆炸
        self.bomb_picture_list = [] #用来存储爆炸时需要的图片
        self.bomb_picture_num = picture_num #飞机爆炸效果的图片数量
        self.image_num = 0#用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0#用来记录当前要显示的爆炸效果的图片的序号
        self.key_down_list = [] #用来存储键盘左右移动键



class BasePlane(Base):
    """docstring for BasePlane"""
    def __init__(self, screen_temp, x, y, image_name, picture_num):
        Base.__init__(self, screen_temp, x, y, image_name, picture_num)
        self.bullet_list = [] #存储发射出去的子弹的引用

    def display(self):
        """显示玩家的飞机"""
        #如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hit == True:
            self.screen.blit(self.bomb_picture_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7: #每７次循环换一张图片
                self.image_num = 0
                self.image_index += 1
            if self.image_index > self.bomb_picture_num-1:
                time.sleep(1)
                exit()#调用exit让游戏退出
        else:
            self.screen.blit(self.image, (self.x, self.y))

        bullet_list_out = []#越界子弹
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge(): #判断子弹是否越界
                bullet_list_out.append(bullet)
        #删除越界子弹
        for bullet in bullet_list_out:
            self.bullet_list.remove(bullet)

    def crate_images(self, bomb_picture_name):
            for i in range(1, self.bomb_picture_num + 1):
                self.bomb_picture_list.append(pygame.image.load("./feiji/" + bomb_picture_name + str(i) + ".png"))

    #判断是否被击中
    def isHitted(self, plane, width, height):# widht和height表示图片的宽、高
        if plane.bullet_list is not None:
            for bullet in plane.bullet_list:
                if bullet.x > self.x and bullet.x < self.x + width and bullet.y > self.y and bullet.y < self.y + height:
                    plane.bullet_list.remove(bullet)
                    self.hit = True



class HeroPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 210, 700, "./feiji/hero1.png", 4) #super().__init__()
        BasePlane.crate_images(self, "hero_blowup_n")

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    #控制飞机左右移动范围
    def move_limit(self):
        if self.x < 0:
            self.x = -2
        elif self.x+100 > 480:
            self.x = 386

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))

    #键盘按下向列表添加左右按键
    def key_down(self, key):
        self.key_down_list.append(key)

    #键盘松开向列表删除左右按键
    def key_up(self, key):
        if len(self.key_down_list) != 0: #判断是否为空
            self.key_down_list.pop(0)

    #当一直按下键盘时调用移动函数
    def press_move(self):
        if len(self.key_down_list) != 0:
            if self.key_down_list[0] == K_LEFT:
                self.move_left()
            elif self.key_down_list[0] == K_RIGHT:
                self.move_right()
    def bomb(self):
        self.hit = True

    #是否击中hero判断
    def hitHero(self, enemy_temp):
        if enemy_temp.bullet_list is not None:
            for bullet in enemy_temp.bullet_list:
                if bullet.x > self.x and bullet.x < self.x+100 and bullet.y > self.y and bullet.y < self.y + 124:
                    enemy_temp.bullet_list.remove(bullet)
                    self.bomb()



class EnemyPlane(BasePlane):
    """敌机的类"""
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./feiji/enemy0.png")
        self.direction = "right" #用来存储飞机默认显示方向

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        # 方向判断
        if self.x > 480-50:
            self.direction ="left"
        elif self.x < 0:
            self.direction = "right"

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num == 8 or random_num == 20:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))


class BaseBullet(Base):
    """docstring for BaseBullet"""
    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+40, y-20, "./feiji/bullet.png")

    def move(self):
        self.y -= 15

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+25, y+40, "./feiji/bullet1.png")

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False

def main():
    #1. 创建窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")

    #3. 创建一个飞机对象
    hero = HeroPlane(screen)

    #4. 创建一个敌机
    enemy = EnemyPlane(screen)

    while True:
        screen.blit(background, (0,0))

        #hero
        hero.display() #hero展示
        hero.press_move()
        hero.move_limit() #hero移动范围判断
        #enemy
        enemy.move() #控制敌机的移动
        enemy.fire() #敌机开火
        enemy.display() #enemy展示

        hero.isHitted(enemy, 100, 124) #是否击中hero
        enemy.isHitted(hero, 51, 39) #是否击中enemy

        pygame.display.update()

        key_control(hero)

        time.sleep(0.01)

if __name__ == "__main__":
    main()
