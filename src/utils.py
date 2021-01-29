import os
import numpy as np
import heapq

def get_path(f):
    dirname = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(dirname, f).replace('/', '\\')

# https://fr.wikipedia.org/wiki/Algorithme_A*
# https://realpython.com/python-heapq-module/

def get_shorter_paths(tentative, positions, through):
    path = tentative[through] + [through]
    for position in positions:
        if position in tentative and len(tentative[position]) <= len(path):
            continue
        yield position, path

def is_valid(mp, position):
    x, y = position
    if not (0 <= y < mp.shape[1] and 0 <= x < mp.shape[0]):
        return False
    if mp[x,y] != '¤' and mp[x,y] != '+' and mp[x,y] != '#':
        return False
    return True

def get_neighbors(mp, current):
    x, y = current
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if dx != 0 and dy != 0:
                continue
            position = x + dx, y + dy
            if is_valid(mp, position):
                yield position

def find_path(mp, origin, destination):
    tentative = {origin: []}
    candidates = [(0, origin)]
    certain = set()
    while destination not in certain and len(candidates) > 0:
        _ignored, current = heapq.heappop(candidates)
        if current in certain:
            continue
        certain.add(current)
        neighbors = set(get_neighbors(mp, current)) - certain
        shorter = get_shorter_paths(tentative, neighbors, current)
        for neighbor, path in shorter:
            tentative[neighbor] = path
            heapq.heappush(candidates, (len(path), neighbor))
        
    if destination in tentative:
        return tentative[destination] + [destination]
    else:
        raise ValueError("no path")
