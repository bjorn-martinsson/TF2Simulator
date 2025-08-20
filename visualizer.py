"""
    Semi-fancy visualizer
"""

import simulation


def visualize(player_pos, rocket_positions = {}, rocket_explosions = {}):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.animation import FuncAnimation
    import numpy as np
    from matplotlib.ticker import MultipleLocator

    data = np.array(player_pos)
    px, py, pz = data[:,0], data[:,1], data[:,2]

    # Set up the figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set limits
    ax.set_xlim(min(px) - 1, max(px) + 1)
    ax.set_ylim(min(py) - 1, max(py) + 1)
    ax.set_zlim(min(pz) - 1, max(pz) + 1)
    
    # Increase grid density
    ax.xaxis.set_major_locator(MultipleLocator(100))
    ax.yaxis.set_major_locator(MultipleLocator(100))
    ax.zaxis.set_major_locator(MultipleLocator(100))
    ax.grid(True)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Line showing path
    ax.plot(px, py, pz, color='lightgray', linewidth=1, marker='x')
    ax.set_aspect('equal')
    
    for rocket_id in rocket_positions:
        data = np.array(rocket_positions[rocket_id])
        x, y, z = data[:,0], data[:,1], data[:,2]
        ax.plot(x, y, z, color='blue', linewidth=1, marker='x')

    for rocket_id in rocket_explosions:
        x,y,z = rocket_explosions[rocket_id]
        ax.plot(x, y, z, color='red', linewidth=1, marker='o')


    ax.view_init(azim=-90, elev=0)#, elev=30)
    
    # Moving ball
    ball, = ax.plot([], [], [], 'ro', markersize=8)

    def init():
        ball.set_data([], [])
        ball.set_3d_properties([])
        return ball,

    def update(frame):
        ball.set_data([px[frame]], [py[frame]])
        ball.set_3d_properties([pz[frame]])
        return ball,

    ani = FuncAnimation(fig, update, frames=len(px), init_func=init,
                        interval=simulation.tick_duration*1000, blit=True, repeat=True)

    plt.show()
