"""
    EXAMPLE

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
    
    def player_before_tick_update(self, p):
        print('At tick %d has pos:' % tick, p.pos)

    def soldier_before_hit(self, p, explosion_dir, modified_damage, explosion_pos):
        print('Update at tick', tick, end = ':\n')
        print('Player hit by rocket, old hspeed is', sqrt(sum(p.vel[i]**2 for i in range(2))))
    
    def soldier_after_hit(self, p, explosion_dir, modified_damage, explosion_pos):
        print('Update at tick', tick, end = ':\n')
        print('Player hit by rocket, new hspeed is', sqrt(sum(p.vel[i]**2 for i in range(2))), p.vel)
    
    # Record player positions
    def soldier_created(self, p):
        player_pos.append(list(p.pos))
    def soldier_after_tick_update(self, p):
        player_pos.append(list(p.pos))

my_key_state = simulation.Key_state()

p = simulation.Soldier(my_key_state, hook=My_hook(), launcher=simulation.Stock)
my_key_state.press_key('+forward')
for tick in range(406):
    p.simulate_tick()
    
    if tick == 20:
        my_key_state.press_key('+attack')

    if tick == 25:
        my_key_state.press_key('+duck')

visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
