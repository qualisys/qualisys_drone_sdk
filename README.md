![qfly | Qualisys Drone SDK](https://qualisys.github.io/qualisys_drone_sdk/qfly_banner.png)

# Qualisys Drone SDK

qfly | Qualisys Drone SDK is a Python library to track and fly drones with [Qualisys motion capture systems](https://qualisys.com/). It is is designed to be an entry point for students, researchers, engineers, artists, and designers to develop drone applications. 

**STATUS: DEV PREVIEW** :: Development and testing is ongoing for many features. For bug reports, feature requests, and other contributions, please use [Issues](https://github.com/mbaytas/qualisys_drone_sdk/issues).

qfly is architected as a concurrent wrapper running the [Qualisys Python SDK](https://github.com/qualisys/qualisys_python_sdk) together with Python libraries for popular drone platforms like [Bitcraze Crazyflie](https://www.bitcraze.io/products/crazyflie-2-1/) and [Robomaster TT](https://www.dji.com/robomaster-tt). It dramatically reduces the software development workload for real-time drone control, compared to using these libraries vanilla form. For creative applications like drone shows, light painting, and cinematography, movements can be easily programmed by non-engineers using principles of keyframe animation. For interactive applications like games and exercise, qfly is able to ingest signals and control drones in real time.

Various safety, stability, and convenience measures are built in, including:

- geofencing
- speed limits
- smooth takeoff and landing
- interrupt and land

qfly can control swarms comprising an arbitrary combination of drones, e.g. [Bitcraze Crazyflie](https://www.bitcraze.io/products/crazyflie-2-1/) and [Ryze Tello EDU](https://www.ryzerobotics.com/tello-edu) drones can be flown together. The maximum number of drones in the swarm depends on limitations of the drone's software and electronics as well as fleet management practicalities.

### Requirements

- [Python](https://www.python.org/) 3.10 or equivalent
- Python packages (install using [pip](https://pypi.org/project/pip/)):
    - [qtm](https://github.com/qualisys/qualisys_python_sdk) (Qualisys Python SDK) 2.1.1 or equivalent
    - [cflib](https://github.com/bitcraze/crazyflie-lib-python) (for Crazyflie Drones) 0.1.18 or equivalent

qfly has been designed and tested on Windows. It may or may not work on other operating systems.

### Setup

To install qfly DEV PREVIEW:

1. Clone the [qfly source code](https://github.com/qualisys/qualisys_drone_sdk) to your local machine.
2. Navigate to the package root directory and install the qfly package in "development mode" by running: `python -m pip install -e .`

# Drone Platforms and Example Scripts

![Bitcraze Crazyflie](https://qualisys.github.io/qualisys_drone_sdk/qfly_cf.png)

## Bitcraze Crazyflie

### Requirements

- [Bitcraze Crazyflie 2.1](https://www.bitcraze.io/products/crazyflie-2-1/)
- For tracking: For best results, we recommend the [Active Marker Deck](https://store.bitcraze.io/collections/decks/products/active-marker-deck). Alternatively, a [Motion Capture Marker Deck](https://store.bitcraze.io/collections/decks/products/motion-capture-marker-deck) is available. Markers can also be mounted on the drone by hand.

### Setup

- Install drivers for both Crazyflie and the Crazyradio dongle using [Zadig](https://zadig.akeo.ie/) following [Bitcraze's instructions](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/usbwindows/).
- To fly multiple drones, assign different radio addresses to them using the [Crazyflie PC client](https://github.com/bitcraze/crazyflie-clients-python). Refer to "Firmware Configuration" in the [Crazyflie PC client docs](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/).\
    - This can be done over the Crazyradio (requires you to know the current radio address, see Bitcraze docs) or over USB (requires Crazyflie driver, see above).
- **Before takeoff with the Crazyflie, always place the drone(s) flat on the floor, with the front pointing in the positive x-direction of the QTM coordinate system.**

- To fly multiple drones, assign different radio addresses to them using the [Crazyflie PC client](https://github.com/bitcraze/crazyflie-clients-python). (Refer to "Firmware Configuration" in the [Crazyflie PC client docs](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/).) This can be done over the Crazyradio (requires you to know the current radio address, see Bitcraze docs) or over USB (requires Crazyflie driver, see above).

- **Before takeoff with the Crazyflie, always place the drone flat on the floor, with its front pointing in the positive x-direction of the QTM coordinate system.**

- In case of emergency, press `Ctrl` + `C` in the terminal window to terminate the program.

- White running the example scripts, Press `Esc` to stop the program and attempt to calmly land the drone.

### Examples

#### [cf_solo.py](examples/cf_solo.py)

This script demonstrates a basic scenario using the Qualisys motion capture system to control the flight path of a Crazyflie. The script commands the Crazyflie to:

1. Take off and hover at the center of its airspace
2. Circle around the Z axis
3. Circle around the Y axis
4. Circle around the X axis
6. Come back to center, land carefully

#### [cf_multi.py](examples/cf_multi.py)

The drones take off and fly circles around Z axis.

*Notice: The swarm scripts have so far been tested with 4 drones. They may or may not work with more drones. Testing with larger swarms is in progress. *

#### [cf_interactive_deck.py](examples/cf_interactive_deck.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of another drone equipped with an [Active Marker Deck](https://www.bitcraze.io/products/active-marker-deck/).

The drone flies along the YZ plane while centered at 0 along the X plane. The Y and Z coordinates track the second Crazyflie.

#### [cf_interactive_traqr.py](examples/cf_interactive_traqr.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of a [Qualisys Traqr](https://www.qualisys.com/accessories/traqr/).

The drone flies along the YZ plane while centered at 0 along the X plane. The Y and Z coordinates track the Traqr.

#### [cf_multi_interactive.py](examples/cf_multi_interactive.py)

This script demonstrates real-time interactive control of a Crazyflie swarm, coupling the drones' flight to the position of a [Qualisys Traqr](https://www.qualisys.com/accessories/traqr/).

The drones take off and fly circles around Z axis. The altitude (z) tracks the Traqr.
ESC to land at any time.


![Tello EDU](https://qualisys.github.io/qualisys_drone_sdk/qfly_tello.png)

## Robomaster TT

Coming soon...

---

# Resources and Inspirations

- Tutorial on [Building Interactions with the Bitcraze Crazyflie and Motion Capture](https://www.baytas.net/blog/crazyflie) by Mehmet Aydın Baytaş
- Fun project: [Santa's Flying Helpers](https://www.bitcraze.io/2021/12/santas-flying-helpers/) by Bitcraze
- [Overview of different positioning systems](https://www.bitcraze.io/2021/05/positioning-system-overview/) you can use with the Bitcraze Crazyflie
- [Notes on the design of Drone Chi](https://www.bitcraze.io/2019/12/designing-dronechi/), a meditative human-drone interaction experiment by Joseph La Delfa

# Contributing

The auto-generated documentation needs to be rebuilt using [pdoc3](https://pdoc3.github.io/) following code contributions. To re-generate the documentation files and place them correctly into the `docs/` folder that is served to the web, use the commands in Windows:

    del docs\*.html
    pdoc qfly --force --html --output-dir docs
    move .\docs\qfly\* .\docs\