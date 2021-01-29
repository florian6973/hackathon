import os
import pygame as pg
from utils import get_path


class Player:
    def __init__(self, name, life=15, damage=3, defense=1, money=5, x=1, y=1):
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
        self.rect.x = 16*x
        self.rect.y = 16*y
        self.coordonnees_x = x
        self.coordonnees_y = y

    def move(self, size):
        if self.direction[0] != 0:
            self.rect.x += self.direction[0]*size
            self.coordonnees_x += self.direction[0]
        if self.direction[1] != 0:
            self.rect.y += self.direction[1]*size
            self.coordonnees_y += self.direction[1]

    def rentrer_mur(self, next_tile):
        if next_tile in ['-', '|', '¤']:
            self.direction = (0, 0)

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
        self.rect.x, self.rect.y = x*16, y*16
        self.direction = (0, 0)
        self.coordonnees_x = x
        self.coordonnees_y = y

    def receive_damage(self, player):
        self.life -= player.damage
        if self.life < 0:
            self.alive = False

    def rentrer_mur(self, next_tile):
        if next_tile in ['-', '|', '¤']:
            self.direction = (0, 0)

    def is_alive(self):
        return self.alive

    def move(self, player, size, next_tiles):
        ecart_x = self.coordonnees_x - player.coordonnees_x
        ecart_y = self.coordonnees_y - player.coordonnees_y
        print(ecart_x, ecart_y)
        if abs(ecart_x) < 5 and abs(ecart_y) < 5:
            directions_possibles = []
            directions_associees = [(1, 0), (-1, 0), (0, -1), (0, 1)]
            for pos, tile in enumerate(next_tiles):
                if tile not in ['-', '|', '¤']:
                    directions_possibles.append(directions_associees[pos])

            if abs(ecart_y) < abs(ecart_x):
                if ecart_x < 0 and (1, 0) in directions_possibles:
                    self.direction = (1, 0)
                elif ecart_x > 0 and (-1, 0) in directions_possibles:
                    self.direction = (-1, 0)
            else:
                if ecart_y > 0 and (0, -1) in directions_possibles:
                    self.direction = (0, -1)
                elif ecart_y < 0 and (0, 1) in directions_possibles:
                    self.direction = (0, 1)
            self.coordonnees_x += self.direction[0]
            self.coordonnees_y += self.direction[1]
            self.rect.x += self.direction[0]*size
            self.rect.y += self.direction[1]*size


class Marchand:
    def __init__(self, objects):
        self.objects = objects

    def remove_object(self, object):
        if object in self.objects:
            self.objects.remove(object)


if __name__ == '__main__':

    T = Player('Tristan')
    T.add_object(['force 3', 'defense 5'])
    print(T)
    T.use_object('force 3')

    E = Evil('E', 10, 5, 3*16, 5*16)
    T.combat(E)
    print(T)
