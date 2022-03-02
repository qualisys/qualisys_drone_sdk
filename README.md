![image](https://user-images.githubusercontent.com/1661078/156165793-8d778cb6-b70a-479b-8289-c36ade7ff41e.png)

quadkit is an entry point for students, researchers, engineers, artists, and designers to start tracking and flying drones using a Qualisys motion capture system.

---

# Box Contents

- 2x Bitcraze Crazyflie Drones
- 1x Bitcraze Antenna
- 2x Bitcraze Spare Parts Bundle
- 2x Qualisys x Bitcraze Active Marker Deck

---

# Setup

## QTM Settings

We recommend the following settings:

- Custom Euler angle definitions:
  - First Rotation Axis: `Z`, Positive Rotation: `Clockwise`, Name: `Yaw`, Angle Range: `-180 to 180 deg.`
  - Second Rotation Axis: `Y`, Positive Rotation: `Counterclockwise`, Name: `Pitch`
  - Third Rotation Axis: `X`, Positive Rotation: `Clockwise`, Name: `Roll`, Angle Range: `-180 to 180 deg.`
- Capture Rate: 100 Hz

## Software Environment

The programming language we prefer for drone scripting is [Python](https://www.python.org/), which should be installed properly in your computer.

Additionally, the following Python packages are required (install them using [pip](https://pypi.org/project/pip/)):

- [qtm](https://github.com/qualisys/qualisys_python_sdk)
- [cflib](https://github.com/bitcraze/crazyflie-lib-python) (for Crazyflie)

---

# Drone Platforms and Starter Scripts

## Bitcraze Crazyflie

**Before takeoff with the Crazyflie, always place the drone flat on the floor, with its front pointing in the positive x-direction of the QTM coordinate system.**

We provide two scripts that demonstrate the Crazyflie integration, which can be used as a starting point for your own projects:

### [crazyflie_solo.py](crazyflie_solo.py)

This script demonstrates a basic scenario using a Qualisys motion capture system to control the flight path of a Crazyflie.

It also runs through the electronic, mechanical, and communications systems of the Crazyflie. It's a good idea to run this script once to check that everything is in order, before executing more complex behavior.

The script commands the Crazyflie to:

1. Take off and hover 1m above its initial position for 30 seconds
2. Move out 50cm in the X direction and complete 2 circles around its initial position
3. For 1 minute, move randomly within a cubic volume that is 1m on each side, centered 1m above its initial position

Pressing the `L` key on the keyboard while the script is running will stop the program and attempt to calmly land the drone. 

### [crazyflie_interactive.py](crazyflie_interactive.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of another object.

### [crazyflie_dual.py](crazyflie_dual.py)

This script demonstrates a semi-choreographed "swarm" flight with two Crazyflie drones.

## DJI Tello

### tello_solo.py

### tello_interactive.py

---

# Resources and Inspirations

- Tutorial on [Building Interactions with the Bitcraze Crazyflie and Motion Capture](https://www.baytas.net/blog/crazyflie) by Mehmet Aydın Baytaş
- Fun project: [Santa's Flying Helpers](https://www.bitcraze.io/2021/12/santas-flying-helpers/) by Bitcraze
- [Overview of different positioning systems](https://www.bitcraze.io/2021/05/positioning-system-overview/) you can use with the Bitcraze Crazyflie
- [Notes on the design of Drone Chi](https://www.bitcraze.io/2019/12/designing-dronechi/), a meditative human-drone interaction experiment by Joseph La Delfa
