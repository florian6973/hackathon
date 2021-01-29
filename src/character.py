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
        self.images = []
        for k in range(1, 9):
            if k != 5:
                self.images.append(pg.image.load(
                    get_path("resx/imgs/wisher" + str(k) + ".png")))
        for k in range(8, 0, -1):
            if k != 5:
                self.images.append(pg.image.load(
                    get_path("resx/imgs/wisher" + str(k) + ".png")))
        self.indice_animation = 0
        self.attaque = False
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

    def combat(self, evil):
        ecart_x = self.coordonnees_x - evil.coordonnees_x
        ecart_y = self.coordonnees_y - evil.coordonnees_y
        if (abs(ecart_x) == 1 and ecart_y == 0) or (ecart_x == 0 and abs(ecart_y) == 1):
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
        self.images = [self.image]
        for k in range(1, 3):
            self.images.append(pg.image.load(
                get_path("resx/imgs/goblin" + str(k) + ".png")))
        for k in range(2, 0, -1):

            self.images.append(pg.image.load(
                get_path("resx/imgs/goblin" + str(k) + ".png")))
        self.indice_animation = 0
        self.direction = (0, 0)
        self.coordonnees_x = x
        self.coordonnees_y = y
        self.fight = False
        self.compteur = 0
        self.attaque = False

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
        self.fight = False
        ecart_x = self.coordonnees_x - player.coordonnees_x
        ecart_y = self.coordonnees_y - player.coordonnees_y
        # print(self.compteur)
        if self.compteur > 0:
            self.compteur -= 1

        if (ecart_x == 0 and abs(ecart_y) == 1) or (abs(ecart_x) == 1 and ecart_y == 0):
            self.fight = True
            if self.compteur == 0:
                self.attaque = True
                player.receive_damage(self)
                self.compteur = 50
                print(player.life)

        if self.alive == True:
            if (abs(ecart_x) < 5 and abs(ecart_y)) < 5 and not self.fight:
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
                self.direction = (0, 0)


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
