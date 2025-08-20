"""
    EXAMPLE 10
    This tests out different kinds of jump, and displays their height 1 tick before touching the floor.
    This is useful for anyone that want to understand how jumping works.

    Here is a quick rundown:
    * You start at 0.03125 units above the floor.
    * Bhopping with a normal jump results in +0.70500
    * Bhopping with a crouched jump results in +0.72000
    * Bhopping with a ctap jump results in -0.005000
    * If you ever go < 0 or > 2, then it resets.

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
for tick in range(1000):
    p.simulate_tick()
    
    if tick == 15:
        print('=============')
        print('Standard jump')
        my_key_state.press_key('+jump')
    if tick == 16:
        my_key_state.release_key('+jump')
    
    if tick == 75:
        print('=============')
        print('Standard jump + land crouched')
        my_key_state.press_key('+jump')
    if tick == 76:
        my_key_state.release_key('+jump')
        my_key_state.press_key('+duck')
    if tick == 130:
        my_key_state.release_key('+duck')

    if tick == 160:
        print('=============')
        print('Crouched jump')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 162:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 210:
        print('=============')
        print('Crouched jump + land crouched')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 212:
        my_key_state.release_key('+jump')
    if tick == 267:
        my_key_state.release_key('+duck')
   
    if tick == 300:
        print('=============')
        print('Ctap + land crouched')
        assert not p.b_ducked
        my_key_state.press_keys('+jump', '+duck')
    if tick == 301:
        my_key_state.release_keys('+jump', '+duck')
    if tick == 302:
        my_key_state.press_key('+duck')
    if tick == 356:
        assert p.b_ducked
        my_key_state.release_key('+duck')

    if tick == 400:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 401:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 450:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 451:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 500:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 501:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 550:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 551:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 600:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 601:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 650:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 651:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 700:
        print('=============')
        print('Ctap')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 701:
        my_key_state.release_keys('+jump', '+duck')

    if tick == 750:
        print('=============')
        print('Crouched jump')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 752:
        my_key_state.release_keys('+jump', '+duck')
    
    if tick == 798:
        print('=============')
        print('Bunny jump crouched jump')
        my_key_state.press_keys('+jump', '+duck')
    if tick == 800:
        my_key_state.release_keys('+jump', '+duck')
visualizer.visualize(player_pos, rocket_positions, rocket_explosions)
