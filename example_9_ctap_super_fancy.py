"""
    EXAMPLE 9
    The best possible ctap.
    Uses original, with 6x "pre-ctaps", with perfect angle.
    The player moves in order to be able to use a lower angle, 
    resulting in the rocket exloding slightly higher up.

    Uses a custom hook to record player positions, rocket positions
    and prints hspeed before and after each rocket hits
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
        print(explosion_dir)

    # Record player positions
    def soldier_created(self, p):
        player_pos.append(list(p.pos))
    def soldier_after_tick_update(self, p):
        player_pos.append(list(p.pos))

my_key_state = simulation.Key_state()

p = simulation.Soldier(my_key_state, hook=My_hook(), launcher=simulation.Original)
p.angle = -88.976
for tick in range(456):
    p.simulate_tick()
   
    if tick == 2:
        my_key_state.press_keys('+jump','+duck')
    if tick == 3:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 52:
        my_key_state.press_keys('+jump','+duck')
    if tick == 53:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 102:
        my_key_state.press_keys('+jump','+duck')
    if tick == 103:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 152:
        my_key_state.press_keys('+jump','+duck')
    if tick == 153:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 202:
        my_key_state.press_keys('+jump','+duck')
    if tick == 203:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 252:
        my_key_state.press_keys('+jump','+duck')
    if tick == 253:
        my_key_state.release_keys('+jump', '+duck')


    if tick == 298:
        my_key_state.press_key('+backward', 1.0)
    if tick == 299:
        my_key_state.press_key('+backward', 1.0)
    if tick == 305:
        my_key_state.release_key('+backward')

    if tick == 325:
        my_key_state.press_key('+attack')
    if tick == 326:
        my_key_state.release_key('+attack')
    
    if tick == 327:
        my_key_state.press_keys('+jump', '+duck')
    if tick == 328:
        my_key_state.release_keys('+jump', '+duck')


print('Max height in jump', max(pos[2] for pos in player_pos))

visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
