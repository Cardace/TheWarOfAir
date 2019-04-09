import pygame
import time
import random
from pygame.locals import *

#全局变量
hit_score = 0
#飞机HP
HP_list = [1, 15, 25, 5]
#敌机子弹类型
bullet_type = ["bullet1.png", "bullet-1.gif", "bullet2.png", "bullet.png"]
#飞机大小
plane_size = [{"width":51, "height":39}, {"width":69, "height":89}, {"width":165, "height":246}, {"width":100, "height":124}, ]
#敌机引用列表
enemy0_list = []#小飞机
enemy0_maximum = 6
enemy1_list = []#boss1
enemy1_maximum = 1
enemy2_list = []#boss2
enemy2_maximum = 1

class Base(object):
    """docstring for Base"""
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)


class BasePlane(Base):
    """docstring for BasePlane"""
    def __init__(self, plane_type, screen_temp, x, y, image_name, picture_num, HP_temp):
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = [] #存储发射出去的子弹的引用
        self.plane_type = plane_type #飞机类型标示, 3是hero
        #爆炸效果用的如下属性
        self.hitted = False #表示是否要爆炸
        self.bomb_picture_list = [] #用来存储爆炸时需要的图片
        self.bomb_picture_num = picture_num #飞机爆炸效果的图片数量
        self.image_num = 0#用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0#用来记录当前要显示的爆炸效果的图片的序号
        self.HP = HP_temp

    def display(self):
        """显示玩家的飞机"""
        global hit_score
        global HP_list
        #如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hitted == True and self.image_index < self.bomb_picture_num and self.HP <= 0:
            if self.plane_type != 3 and self.image_index == 0 and self.image_num == 0:
                hit_score += HP_list[self.plane_type]
            self.screen.blit(self.bomb_picture_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7: #每7次循环换一张图片
                self.image_num = 0
                self.image_index += 1
            # if self.image_index > self.bomb_picture_num-1:
            #     # time.sleep(1)
            #     # del_plane(self)
            #     # exit()#调用exit让游戏退出
            #     pass
        elif self.image_index < self.bomb_picture_num:
            self.screen.blit(self.image, (self.x, self.y))
        if self.hitted == True and not self.bullet_list and self.image_index >= self.bomb_picture_num:
            del_plane(self) #删除被击中敌机的对象
        bullet_list_out = []#越界子弹
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge(): #判断子弹是否越界
                bullet_list_out.append(bullet)
        #删除越界子弹
        for bullet in bullet_list_out:
            self.bullet_list.remove(bullet)
    #创建出爆炸效果的图片的引用
    def crate_images(self, bomb_picture_name):
            for i in range(1, self.bomb_picture_num + 1):
                self.bomb_picture_list.append(pygame.image.load("./feiji/" + bomb_picture_name + str(i) + ".png"))

    #判断是否被击中
    def isHitted(self, plane, width, height):# widht和height表示范围
        if plane.bullet_list:
            for bullet in plane.bullet_list:
                if bullet.x > self.x+8 and bullet.x < self.x + width and bullet.y+8 > self.y and bullet.y < self.y + height:
                    plane.bullet_list.remove(bullet) #删除击中的子弹
                    self.hitted = True
                    self.HP -= 1


class HeroPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, 3, screen_temp, 210, 700, "./feiji/hero1.png", 4, HP_list[3]) #super().__init__()
        BasePlane.crate_images(self, "hero_blowup_n")
        self.key_down_list = [] #用来存储键盘左右移动键

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    #控制飞机左右移动范围
    def move_limit(self):
        if self.x < 0:
            self.x = -2
        elif self.x + 100 > 480:
            self.x = 380

    def fire(self):
        if len(self.bullet_list) < 5:
            # print("bullet_list=%d"%len(self.bullet_list))
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
        self.hitted = True

    # #是否击中hero判断
    # def hitHero(self, enemy_temp):
    #     if enemy_temp.bullet_list is not None:
    #         for bullet in enemy_temp.bullet_list:
    #             if bullet.x > self.x and bullet.x < self.x+100 and bullet.y > self.y and bullet.y < self.y + 124:
    #                 enemy_temp.bullet_list.remove(bullet)
    #                 self.bomb()



class Enemy0Plane(BasePlane):
    """敌机的类"""
    def __init__(self, screen_temp):
        random_num_x = random.randint(0, 430)
        random_num_y = random.randint(-50, -40)
        BasePlane.__init__(self, 0, screen_temp, random_num_x, random_num_y, "./feiji/enemy0.png", 4, HP_list[0])
        BasePlane.crate_images(self, "enemy0_down")

    def move(self):
        self.y += 2

    def fire(self):
        if not self.hitted:
            random_num = random.randint(1, 200)
            if random_num == 8 or random_num == 70 and len(self.bullet_list) < 3:
                self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y, self))


class Enemy1Plane(BasePlane):
    """敌机的类"""
    def __init__(self, screen_temp):
        BasePlane.__init__(self, 1, screen_temp, 205, -90, "./feiji/enemy1.png", 4, HP_list[1])
        BasePlane.crate_images(self, "enemy1_down")
        self.direction = "right" #用来存储飞机默认显示方向


    def move(self):
        if self.direction == "right":
            self.x += 3
        elif self.direction == "left":
            self.x -= 3
        # 方向判断
        if self.x+70 > 480:
            self.direction ="left"
        elif self.x < 0:
            self.direction = "right"
        if self.y < 50:
            self.y += 3

    def fire(self):
        random_num = random.randint(1, 100)
        if random_num == 8 or random_num == 70 and len(self.bullet_list) < 6:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y, self))


class Enemy2Plane(BasePlane):
    """敌机的类"""
    def __init__(self, screen_temp):
        BasePlane.__init__(self, 2, screen_temp, 158, -246, "./feiji/enemy2.png", 5, HP_list[2])
        BasePlane.crate_images(self, "enemy2_down")
        self.direction = "right" #用来存储飞机默认显示方向

    def move(self):
        if self.direction == "right":
            self.x += 2
        elif self.direction == "left":
            self.x -= 2
        # 方向判断
        if self.x+165 > 480:
            self.direction ="left"
        elif self.x < 0:
            self.direction = "right"
        if self.y < 0:
            self.y += 2

    def fire(self):
        random_num = random.randint(1, 50)
        if random_num == 8 or random_num == 40 and len(self.bullet_list) < 9:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y, self))

class BaseBullet(Base):
    """docstring for BaseBullet"""
    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+40, y-14, "./feiji/bullet.png")

    def move(self):
        self.y -= 12

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False


class EnemyBullet(BaseBullet):
    global bullet_type
    global plane_size
    def __init__(self, screen_temp, x, y, plane):
        BaseBullet.__init__(self, screen_temp, x+plane_size[plane.plane_type]["width"]/2, y+plane_size[plane.plane_type]["height"]/2, "./feiji/"+bullet_type[plane.plane_type])

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False

def del_plane(plane):
    """回收被击中的敌机的对象"""
    global hit_score
    global enemy0_list
    global enemy1_list
    global enemy2_list

    if plane in enemy0_list:
        enemy0_list.remove(plane)
    elif plane in enemy1_list:
        enemy1_list.remove(plane)
    elif plane in enemy2_list:
        enemy2_list.remove(plane)

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

def main():
    global hit_score
    global HP_list
    global enemy0_list
    global enemy0_maximum
    global enemy1_list
    global enemy1_maximum
    global enemy2_list
    global enemy2_maximum

    hit_score_temp = hit_score

    #1. 创建窗口
    screen = pygame.display.set_mode((480,852),0,32)

    #2. 创建一个背景图片
    background = pygame.image.load("./feiji/background.png")

    #3. 创建一个飞机对象
    hero = HeroPlane(screen)

    #4. 创建一个敌机
    # enemy = Enemy0Plane(screen)

    while True:
        if hit_score > hit_score_temp:
            hit_score_temp = hit_score
            print("得分: %d"%hit_score)
        #创建敌机
        random_num = random.randint(1, 100)
        if random_num == 29 or random == 50 and len(enemy0_list) < enemy0_maximum:
            enemy0_list.append(Enemy0Plane(screen))
            enemy0_maximum += 1
        if hit_score >= 20 and (hit_score%20) == 0 and len(enemy1_list) < enemy1_maximum:
            enemy1_list.append(Enemy1Plane(screen))
        # if len(enemy1_list) < enemy1_maximum:
        #     enemy1_list.append(Enemy1Plane(screen))
        if hit_score >= 85 and (hit_score%85) == 0 and len(enemy2_list) < enemy2_maximum:
            enemy2_list.append(Enemy2Plane(screen))

        screen.blit(background, (0,0))

        #hero
        hero.display() #hero展示
        hero.press_move()
        hero.move_limit() #hero移动范围判断

        if enemy0_list:
            for enemy0 in enemy0_list:
                enemy0.move() #控制敌机的移动
                enemy0.fire() #敌机开火
                enemy0.display() #enemy展示
                hero.isHitted(enemy0, 92, 116) #是否击中hero
                enemy0.isHitted(hero, 43, 31) #是否击中enemy
        if enemy1_list:
            for enemy1 in enemy1_list:
                enemy1.move() #控制敌机的移动
                enemy1.fire() #敌机开火
                enemy1.display() #enemy展示
                hero.isHitted(enemy1, 92, 116) #是否击中hero
                enemy1.isHitted(hero, 61, 71) #是否击中enemy
        if enemy2_list:
            for enemy2 in enemy2_list:
                enemy2.move() #控制敌机的移动
                enemy2.fire() #敌机开火
                enemy2.display() #enemy展示
                hero.isHitted(enemy2, 92, 116) #是否击中hero
                enemy2.isHitted(hero, 147, 238) #是否击中enemy

        # print("enemy2: %d"%len(enemy2_list))

        pygame.display.update()

        key_control(hero)

        time.sleep(0.01)

if __name__ == "__main__":
    main()
