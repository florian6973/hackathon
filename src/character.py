import os
import pygame as pg
from utils import get_path


class Player:
    def __init__(self, name, life=15, damage=3, defense=1, money=5):
        self.name = name
        self.life = life
        self.inventory = []
        self.damage = damage
        self.defense = defense
        self.alive = True
        self.money = money
        self.image = pg.image.load(get_path("resx/imgs/wisher.png"))
        self.rect = self.image.get_rect()
        self.direction = (0, 0)

    def move(self, size):
        if self.direction[0] != 0:
            self.rect.x += self.direction[0]*size
        if self.direction[1] != 0:
            self.rect.y += self.direction[1]*size

    def rentrer_mur(self, next_tile):
        if next_tile in ['-', '|', '¤']:
            self.direction = (0,0)
        

    def receive_damage(self, evil):
        if evil.damage - self.defense > 0:
            self.life -= evil.damage - self.defense

        if self.life <= 0:
            self.alive = False

    def combat(self, evil):
        while self.life > 0 and evil.life > 0:
            evil.receive_damage(self)
            if evil.alive:
                self.receive_damage(evil)

    def is_alive(self):
        return self.alive

    def add_object(self, objects):
        if type(objects) == list:
            for object in objects:
                self.inventory.append(object)
        else:
            self.inventory.append(objects)

    def add_money(self, argent):
        self.money += argent

    def use_object(self, object):

        if object in self.inventory:
            self.inventory.remove(object)
            name, strength = object.split(' ')
            if name == 'vie':
                self.life += int(strength)
            if name == 'force':
                self.damage += int(strength)
            if name == 'defense':
                self.defense += int(strength)

    def buy_object(self, marchand, object):
        if object in marchand.objects:
            stuff, cost = object
            marchand.remove_object(object)
            if self.money >= cost:
                self.inventory.append(stuff)
                self.money -= cost

    def __repr__(self):
        return f'name {self.name} life {self.life} damage {self.damage} defense {self.defense} invent {self.inventory}'


class Evil:
    def __init__(self, name, life, damage, x, y):
        self.name = name
        self.life = life
        self.damage = damage
        self.alive = True
        self.image = pg.image.load(get_path("resx/imgs/goblin.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def receive_damage(self, player):
        self.life -= player.damage
        if self.life < 0:
            self.alive = False

    def is_alive(self):
        return self.alive

    def move(self, player):
        if abs(self.rect.x - player.rect[0]) and abs(self.rect.y - player.rect[1]):
            self.rect.x = x
            self.rect.y = y


class Marchand:
    def __init__(self, objects):
        self.objects = objects

    def remove_object(self, object):
        if object in self.objects:
            self.objects.remove(object)


if __name__ == '__main__':

    T = Player('Tristan')
    T.add_object(['force 10', 'defense 5'])
    print(T)
    T.use_object('force 10')

    E = Evil('E', 10, 5, 3*16, 5*16)
    T.combat(E)
    print(T)
