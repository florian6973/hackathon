import os
import pygame as pg
from utils import get_path


class Player:
    def __init__(self, name):
        self.name = name
        self.life = 15
        self.inventory = []
        self.damage = 1
        self.defense = 1
        self.alive = True
        self.money = 5
        self.image = pg.image.load(get_path("resx/imgs/wisher.png"))
        self.rect = self.image.get_rect()

    def receive_damage(self, damage):
        self.life -= damage - self.defense

        if self.life <= 0:
            self.alive = False

    def is_alive(self):
        return self.alive

    def add_object(self, objects):
        if type(objects) == list:
            for object in objects:
                self.inventory.append(object)
        else:
            self.inventory.append(objects)

    def add_money(self, coin):
        self.money += coin

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
            if money >= cost:
                self.inventory.append(object)
                self.money -= cost

    def __repr__(self):
        return f'{self.name} {self.life} {self.damage} {self.inventory}'


class Evil:
    def __init__(self, name):
        self.name = name


class Marchand:
    def __init__(self, objects):
        self.objects = objects

    def remove_object(self, object):
        if object in self.objects:
            self.objects.remove(object)


T = Player('Tristan')
T.add_object(['force 10', 'defense 5'])
print(T)
T.use_object('force 10')
T.receive_damage(4)
print(T)
