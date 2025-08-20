"""
    EXAMPLE 3
    Jump_speed2 lvl 8, standard jump off into jump bug

    Uses a custom hook to record player positions, rocket positions
    and prints hspeed before and after each rocket hits
    Prints info when a jump bug is possible/hit
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

    # The player could jump bug
    def player_jumpbug_possible(self, player):
        print('Update at tick', tick, end = ':\n')
        print('Player could jump bug')
    
    # The player hits jump bug
    def player_jumpbug_detected(self, player):
        print('Update at tick', tick, end = ':\n')
        print('Player did a jump bug')

    # On jump
    def player_ground_to_air(self, p):
        # Change floor to bottom floor 
        p.floor = floor2
        print('Update at tick', tick, end = ':\n')
        print('Player left ground')

    # Record player positions
    def soldier_created(self, p):
        player_pos.append(list(p.pos))
    def soldier_after_tick_update(self, p):
        player_pos.append(list(p.pos))

my_key_state = simulation.Key_state()

initial_pos = [.0, .0, 1088.0]
floor1 = simulation.Floor(1088.0)
floor2 = simulation.Floor(0.0)

p = simulation.Soldier(my_key_state, hook=My_hook(), pos=initial_pos, floor=floor1)
my_key_state.press_key('+forward')
for tick in range(406):
    p.simulate_tick()
    
    if tick == 15:
        my_key_state.press_key('+jump')
    
    if tick == 16:
        my_key_state.release_key('+jump')
        my_key_state.press_key('+duck')

    if tick == 151:
        my_key_state.release_key('+duck')
        my_key_state.press_key('+jump')

visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
