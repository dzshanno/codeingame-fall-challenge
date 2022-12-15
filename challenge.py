import sys
import math
from dataclasses import dataclass

ME = 1
OPP = 0
NONE = -1
time = 0

@dataclass
class Tile:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool

width, height = [int(i) for i in input().split()]

def distance(t1,t2):
    separation = math.sqrt((t2.x-t1.x)**2+(t2.y-t1.y)**2)
    return separation

def closest_spawn():
    closest_tile = [my_tiles[0]]
    closest_distance = 10_000_000
    if len(opp_tiles) == 0:
        return False
    for mt in my_tiles:
        for ou in opp_units:
            if distance(mt,ou) < closest_distance:
                closest_distance = distance(mt,ou)
                closest_tile = mt
   
    return closest_tile

def furthest_spawn():
    furthest_tile = [my_tiles[0]]
    furthest_distance = 0
    if len(opp_tiles) == 0:
        return False
    for mt in my_tiles:
        for ou in opp_units:
            if distance(mt,ou) > furthest_distance:
                furthest_distance = distance(mt,ou)
                furthest_tile = mt
   
    return furthest_tile


        
# game loop
while True:
    time = time + 1
    tiles = []
    my_units = []
    opp_units = []
    my_recyclers = []
    opp_recyclers = []
    opp_tiles = []
    my_tiles = []
    neutral_tiles = []

    my_matter, opp_matter = [int(i) for i in input().split()]
    for y in range(height):
        for x in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            # recycler, can_build, can_spawn, in_range_of_recycler: 1 = True, 0 = False
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            tile = Tile(x, y, scrap_amount, owner, units, recycler == 1, can_build == 1, can_spawn == 1, in_range_of_recycler == 1)

            tiles.append(tile)

            if tile.owner == ME:
                my_tiles.append(tile)
                if tile.units > 0:
                    my_units.append(tile)
                elif tile.recycler:
                    my_recyclers.append(tile)
            elif tile.owner == OPP:
                opp_tiles.append(tile)
                if tile.units > 0:
                    opp_units.append(tile)
                elif tile.recycler:
                    opp_recyclers.append(tile)
            else:
                neutral_tiles.append(tile)

    actions = []
    if len(opp_units) != 0:
        cs = closest_spawn()
        fs = furthest_spawn()
        for tile in my_tiles:
            if time % 3 == 0:
                if tile.can_spawn:
                
                    if len(opp_tiles) == 0:
                        amount = 0
                    else:
                        amount = 1 # TODO: pick amount of robots to spawn here
                    if amount > 0:
                        actions.append('SPAWN {} {} {}'.format(amount, cs.x, cs.y))
        for tile in my_tiles:
            if time % 5 ==0:
                if tile.can_build:
                    should_build = False
                    if fs == tile:
                        should_build = True # TODO: pick whether to build recycler here
                    if should_build:
                        actions.append('BUILD {} {}'.format(tile.x, tile.y))
        
        i=0
        for tile in my_units:
            no_of_opp = len(opp_units)
            if no_of_opp == 0:
                target = False
            else:
                target = opp_units[i % no_of_opp] # chase equivalent opp
            if target:
                amount = 1 # TODO: pick amount of units to move
                actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target.x, target.y))
            i = i + 1
    else:
        i=0
        for tile in my_units:
            no_of_opp = len(opp_tiles)
            if no_of_opp == 0:
                target = False
            else:
                target = opp_tiles[i % no_of_opp]
            if target:
                amount = 1 # TODO: pick amount of units to move
                actions.append('MOVE {} {} {} {} {}'.format(amount, tile.x, tile.y, target.x, target.y))
            i = i + 1


    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(';'.join(actions) if len(actions) > 0 else 'WAIT')