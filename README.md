![image](https://user-images.githubusercontent.com/1661078/163686571-606a0648-46dc-437f-9287-474c41bfa858.png)

# Qualisys Drone SDK

**WARNING: This project is under development. Do not expect anything to work.**

<!-- an entry point for students, researchers, engineers, artists, and designers to start tracking and flying drones using a Qualisys motion capture system. -->

---

<!-- # Box Contents

- 2x Bitcraze Crazyflie Drones
- 1x Bitcraze Antenna
- 2x Bitcraze Spare Parts Bundle
- 2x Qualisys x Bitcraze Active Marker Deck

--- -->

# Setup

## Software Environment and Drivers

qfly has been designed and tested on Windows. It may or may not work on other operating systems.

[Python](https://www.python.org/) version 3.10 or equivalent should be installed properly on your computer.

The following Python packages are required (install them using [pip](https://pypi.org/project/pip/)):

- [qtm](https://github.com/qualisys/qualisys_python_sdk) (Qualisys Python SDK) 2.1.1 or equivalent
- [cflib](https://github.com/bitcraze/crazyflie-lib-python) (for Crazyflie Drones) 0.1.18 or equivalent

# Drone Platforms and Example Scripts

## Bitcraze Crazyflie

We provide 3 example scripts for the Crazyflie integration, which can be used as a starting point for your own projects.

We recommend the [Active Marker Deck](https://store.bitcraze.io/collections/decks/products/active-marker-deck) for tracking the drones. Alternatively, a [Motion Capture Marker Deck](https://store.bitcraze.io/collections/decks/products/motion-capture-marker-deck) is available. In most situations, active markers achieve better results.

### Setup

- Install drivers for both Crazyflie and the Crazyradio dongle using [Zadig](https://zadig.akeo.ie/) following [Bitcraze's instructions](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/usbwindows/).

- **Before takeoff with the Crazyflie, always place the drone flat on the floor, with its front pointing in the positive x-direction of the QTM coordinate system.**

- To fly multiple drones, assign different radio addresses to them using the [Crazyflie PC client](https://github.com/bitcraze/crazyflie-clients-python). (Refer to "Firmware Configuration" in the [Crazyflie PC client docs](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/).) This can be done over the Crazyradio (requires you to know the current radio address, see Bitcraze docs) or over USB (requires Crazyflie driver, see above).

- Everything has been tested at a capture rate of 100 Hz.

### [crazyflie_solo.py](crazyflie_solo.py)

This script demonstrates a basic scenario using the Qualisys motion capture system to control the flight path of a Crazyflie. The script commands the Crazyflie to:

1. Take off and hover at the center of its airspace
2. Move out half the radius of the airspace and circle around the Z axis
3. Come back to center, move out half the radius of the airspace and circle around the Y axis
4. Come back to center, move out half the radius of the airspace and circle around the X axis
5. Come back to center, execute a 3D random walk
6. Come back to center, land carefully

Press `Esc` to stop the program and attempt to calmly land the drone. 

### [crazyflie_multi.py](crazyflie_dual.py)

This script demonstrates a semi-choreographed "swarm" flight with two Crazyflie drones.

The drones execute movements that are very similar to the solo script, but with multiple drones together.

Press `Esc` to stop the program and attempt to calmly land the drones. 

### [crazyflie_interactive.py](crazyflie_interactive.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of another object.

In addition to the drone, it requires a "controller" rigid body configured in QTM. We recommend the [Qualisys Traqr range](https://www.qualisys.com/accessories/traqr/).

Press `Esc` to stop the program and attempt to calmly land the drone. 


## DJI Tello

### tello_solo.py

### tello_interactive.py

---

# Resources and Inspirations

- Tutorial on [Building Interactions with the Bitcraze Crazyflie and Motion Capture](https://www.baytas.net/blog/crazyflie) by Mehmet Aydın Baytaş
- Fun project: [Santa's Flying Helpers](https://www.bitcraze.io/2021/12/santas-flying-helpers/) by Bitcraze
- [Overview of different positioning systems](https://www.bitcraze.io/2021/05/positioning-system-overview/) you can use with the Bitcraze Crazyflie
- [Notes on the design of Drone Chi](https://www.bitcraze.io/2019/12/designing-dronechi/), a meditative human-drone interaction experiment by Joseph La Delfa
