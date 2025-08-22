"""
    EXAMPLE 14
    This simulates a setup to jump higher than usual. 
    This abuses TF2 "bunnyjump prevention" to jump higher.
    This bug is described in review.pdf.

    Some reference numbers: 
    You start at 0.03125 units above the floor.
    Bhopping with a normal jump results in +0.70500
    Bhopping with a crouched jump results in +0.72000
    Bhopping with a ctap jump results in -0.005000
    If you ever go < 0 or > 2, then it resets.

    At 316 speed, a jump instead becomes +1.0805.

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
        print('Jump 1, a normal jump')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 17:
        my_key_state.release_keys('+jump', '+duck')

    if tick == 20:
        print('Artifically boosting speed')
        print('Speed before:', p.vel[0])
        p.vel[0] += 76.0
        print('Speed after:', p.vel[0])
    
    if tick == 63:
        print('=============')
        print('Jump 2, a normal jump')
        my_key_state.press_key('+jump')
    if tick == 65:
        my_key_state.release_key('+jump')
    
    if tick == 110:
        print('=============')
        print('Jump 3, a crouch jump')
        my_key_state.press_keys('+jump', '+duck')
    
print('Max height reached', max(pos[2] for pos in player_pos))
visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
