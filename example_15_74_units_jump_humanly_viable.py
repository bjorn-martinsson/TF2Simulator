"""
    EXAMPLE 15
    This simulates a setup to jump higher than usual. 
    Requiring 5 tick perfect inputs while strafing.
    This should be humanly viable.

    Here are some numbers for reference: 
    You start at 0.03125 units above the floor.
    Bhopping with a normal jump results in +0.70500
    Bhopping with a crouched jump results in +0.72000
    Bhopping with a ctap jump results in -0.005000
    If you ever go < 0 or > 2, then it resets.

    The trick is that the 4th jump is about +1.26 because of
    TF2's "bunnyjump prevention" making that jump be higher.

    Uses a custom hook to record player positions, rocket positions
    and prints hspeed before and after each rocket hits
    Prints info when landing.
"""

import simulation
import visualizer
from math import sqrt

from collections import defaultdict
rocket_positions = defaultdict(list)
rocket_explosions = {}
player_pos = []

class My_hook(simulation.Hook_Base):
    # Record rocket positions, and keep track if they explode
    def rocket_creation(self, rocket):
        rocket_positions[rocket.rocket_id].append(list(rocket.pos))
    def rocket_after_tick_update(self, rocket):
        rocket_positions[rocket.rocket_id].append(list(rocket.pos))
    def rocket_exploded(self, rocket, explosion_pos):
        rocket_positions[rocket.rocket_id].append(list(explosion_pos))
        rocket_explosions[rocket.rocket_id] = list(explosion_pos)

    def soldier_before_hit(self, p, explosion_dir, modified_damage, explosion_pos):
        print('Update at tick', tick, end = ':\n')
        print('Player hit by rocket, old hspeed is', sqrt(sum(p.vel[i]**2 for i in range(2))))
    
    def soldier_after_hit(self, p, explosion_dir, modified_damage, explosion_pos):
        print('Update at tick', tick, end = ':\n')
        print('Player hit by rocket, new hspeed is', sqrt(sum(p.vel[i]**2 for i in range(2))), p.vel)

    def soldier_ss_detected(self, p, explosion_dir, modified_damage, explosion_pos):
        print('Update at tick', tick, end = ':\n')
        print('Player hit ss, speed increase by', modified_damage, 'units/s')

    # On landing
    def player_air_to_ground(self, p):
        print('Update at tick', tick, end = ':\n')
        print('Player z at landing %f -> %f (would have been %f if not floor existed)' % (player_pos[-1][2], p.pos[2], player_pos[-1][2] + p.vel[2] * simulation.tick_duration))

    # Record player positions
    def soldier_created(self, p):
        player_pos.append(list(p.pos))
    def soldier_after_tick_update(self, p):
        player_pos.append(list(p.pos))

my_key_state = simulation.Key_state()

p = simulation.Soldier(my_key_state, hook=My_hook())
p.b_on_ground = True
my_key_state.press_key('+forward')
for tick in range(300):
    p.simulate_tick()
    
    if tick == 15:
        print('=============')
        print('Jump 1, a ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 16:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 20:
        print('Artifically boosting speed')
        print('Speed before:', p.vel[0])
        p.vel[0] += 24.0
        print('Speed after:', p.vel[0])

    if tick == 58:
        print('=============')
        print('Jump 2, a ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 59:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 65:
        print('Artifically boosting speed')
        print('Speed before:', p.vel[0])
        p.vel[0] += 24.0
        print('Speed after:', p.vel[0])

    if tick == 101:
        print('=============')
        print('Jump 3, a normal jump')
        my_key_state.press_key('+jump')
    if tick == 103:
        my_key_state.release_key('+jump')
    
    if tick == 105:
        print('Artifically boosting speed')
        print('Speed before:', p.vel[0])
        p.vel[0] += 44.0
        print('Speed after:', p.vel[0])
    
    if tick == 148:
        print('=============')
        print('Jump 4, a normal jump')
        my_key_state.press_key('+jump')
    if tick == 150:
        my_key_state.release_key('+jump')
    
    if tick == 195:
        print('=============')
        print('Jump 5, a crouch jump')
        my_key_state.press_keys('+jump', '+duck') 

    
print('Max height reached', max(pos[2] for pos in player_pos))
visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
