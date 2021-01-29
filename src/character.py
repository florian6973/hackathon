import pygame as pg


class Player:
    def __init__(self, name):
        self.name = name
        self.life = 15
        self.inventory = []
        self.damage = 1
        self.defense = 1
        self.alive = True

    def receive_damage(self, damage):
        self.life -= damage

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

    def use_object(self, object):

        if object in self.inventory:
            self.inventory.remove(object)
            name, strength = object.split(' ')
            if name == 'vie':
                self.life += int(strength)
            if name == 'force':
                self.damage += int(strength)

    def __repr__(self):
        return f'{self.name} {self.life} {self.damage} {self.inventory}'


T = Player('Tristan')
T.add_object('force 10')
print(T)
T.use_object('force 10')
print(T)
