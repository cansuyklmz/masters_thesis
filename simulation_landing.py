import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R
# import classes
import ship_class
import vsqp_class


def draw_drone_3d(ax, drone_state, r=1.0):
    """
    Simplified function to draw a drone as a cross with circles at the end to represent rotors.
    ax: Matplotlib 3D axis to draw on.
    drone_state: The state of the drone including position and orientation.
    r: Scale factor for the drone size.
    """
    # Drone position and orientation
    pos = drone_state[0:3]
    yaw, pitch, roll = drone_state[6:9]

    # Drone body - represented as a cross
    offsets = np.array([[r, 0, 0], [-r, 0, 0], [0, r, 0], [0, -r, 0]])
    for offset in offsets:
        ax.plot3D(*zip(pos, pos + offset), color='black')

    # Rotors - represented as points
    rotor_offsets = offsets * 1.2  # slightly offset from the body
    for rotor_offset in rotor_offsets:
        ax.scatter(*(pos + rotor_offset), color='blue', s=50)

# Function to update both platforms and drone in the animation
def update(frame, ax, platform_simulator, drone_simulator):
    ax.cla()  # Clear the axes
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-5, 5)

    # Update and draw platforms
    positions, headings, pitches, rolls = platform_simulator.update()
    draw_platforms(ax, positions, headings, pitches, rolls, platform_simulator.edge_length)
    
    # Update and draw drone
    actions = np.array([0,0,-9.81])  # Example action, you'll likely calculate this differently
    drone_state = drone_simulator.update(actions)
    draw_drone_3d(ax, drone_state[0])  # Assuming the first environment for simplicity

    return ax,

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initialize both simulators
platform_simulator = PlatformSimulator3D(edge_length=5.0)
drone_simulator = VSQP(num_envs=1, states=np.array([0,0,3,0,0,0,0,0,0]), tau=1, time_step=0.1)

# Create an animation
ani = FuncAnimation(fig, update, fargs=(ax, platform_simulator, drone_simulator), frames=np.arange(0, 100), blit=False, interval=100)

plt.show()
