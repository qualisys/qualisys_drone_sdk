![qfly | Qualisys Drone SDK](https://qualisys.github.io/qualisys_drone_sdk/qfly_banner.png)

# Qualisys Drone SDK

qfly | Qualisys Drone SDK is a Python library to track and fly drones with [Qualisys motion capture systems](https://qualisys.com/). It is designed to be an entry point for students, researchers, engineers, artists, and designers to develop drone applications. 

**STATUS: ALPHA** :: Core functionality is reasonably stable, but development and testing is ongoing for more features. For bug reports, feature requests, and other contributions, please use [Issues](https://github.com/qualisys/qualisys_drone_sdk/issues).

qfly is architected as a concurrent wrapper running the [Qualisys Python SDK](https://github.com/qualisys/qualisys_python_sdk) together with Python libraries for drone platforms. Currently the [Bitcraze Crazyflie](https://www.bitcraze.io/products/crazyflie-2-1/) is supported, while support for [Robomaster TT](https://www.dji.com/robomaster-tt) may be added in the future.

qfly dramatically reduces the software development workload for real-time drone control, compared to using these libraries vanilla form. For creative applications like drone shows, light painting, and cinematography, movements can be easily programmed by non-engineers using principles of keyframe animation. For interactive applications like games and exercise, qfly is able to ingest signals and control drones in real time.

Various safety, stability, and convenience measures are built in, including:

- virtual geofencing
- speed limits
- smooth takeoff and landing
- interrupt and land

qfly can control swarms comprising an arbitrary combination of drones, e.g. [Bitcraze Crazyflie](https://www.bitcraze.io/products/crazyflie-2-1/) and [Robomaster TT](https://www.dji.com/robomaster-tt) drones can be flown together. (Currently qfly provides classes to control the Bitcraze Crazyflie, while other drone platforms require the programmer to import and incorporate their own libraries into their scripts.) The maximum number of drones in the swarm depends on limitations of the drone's software and electronics as well as fleet management practicalities.

### Requirements

- [Python](https://www.python.org/) 3.10 or equivalent
- Python packages:
    - [cflib](https://github.com/bitcraze/crazyflie-lib-python) (for Crazyflie Drones) 0.1.18 or equivalent
    - [qtm](https://github.com/qualisys/qualisys_python_sdk) (Qualisys Python SDK) 2.1.1 or equivalent
    - [pynput](https://github.com/moses-palmer/pynput)  1.7.6 or equivalent

qfly has been designed and tested on Windows.

### Setup

Install using pip:

    pip install qfly

# Drone Platforms and Example Scripts

![Bitcraze Crazyflie](https://qualisys.github.io/qualisys_drone_sdk/qfly_cf.png)

## Bitcraze Crazyflie

### Requirements

- [Bitcraze Crazyflie 2.1](https://www.bitcraze.io/products/crazyflie-2-1/)
- For tracking: For best results, we recommend the [Active Marker Deck](https://store.bitcraze.io/collections/decks/products/active-marker-deck). Alternatively, a [Motion Capture Marker Deck](https://store.bitcraze.io/collections/decks/products/motion-capture-marker-deck) is available. Markers can also be mounted on the drone by hand.

### Setup

- Install drivers for both Crazyflie and the Crazyradio dongle using [Zadig](https://zadig.akeo.ie/) following [Bitcraze's instructions](https://www.bitcraze.io/documentation/repository/crazyradio-firmware/master/building/usbwindows/).
- To fly multiple drones, assign different radio addresses to them using the [Crazyflie PC client](https://github.com/bitcraze/crazyflie-clients-python). (Refer to "Firmware Configuration" in the [Crazyflie PC client docs](https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/).)
    - This can be done over the Crazyradio (requires you to know the current radio address, see Bitcraze docs) or over USB (requires Crazyflie driver, see above).
- *IMPORTANT:* Before takeoff with the Crazyflie, always place the drone flat on the floor, with its front pointing in the positive x-direction of the QTM coordinate system.

### How To Use Example Scripts and What They Do

- In case of emergency, press `Ctrl` + `C` in the terminal window to terminate the program.
- White running the example scripts, Press `Esc` to stop the program and attempt to calmly land the drone.
- The swarm scripts have so far been tested with up to 4 drones.

#### [cf_solo.py](examples/cf_solo.py)

This script demonstrates a basic scenario using the Qualisys motion capture system to control the flight path of a Crazyflie drone.

The script commands the drone to:

1. Take off and hover at the center of its airspace
2. Circle around the Z axis
3. Circle around the Y axis
4. Circle around the X axis
6. Come back to center, land carefully

#### [cf_multi.py](examples/cf_multi.py)

This script demonstrates a basic scenario using the Qualisys motion capture system to control the flight path of two Crazyflie drones.

The script commands the drones to take off and fly circles around Z axis.

#### [cf_interactive_deck.py](examples/cf_interactive_deck.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of another drone equipped with an [Active Marker Deck](https://www.bitcraze.io/products/active-marker-deck/).

The drone is commanded to fly along the YZ plane while centered at 0 along the X plane. The Y and Z coordinates track the Y-Z position second Crazyflie.

#### [cf_interactive_traqr.py](examples/cf_interactive_traqr.py)

This script demonstrates real-time interactive control of a Crazyflie, coupling the drone's flight to the position of a [Qualisys Traqr](https://www.qualisys.com/accessories/traqr/).

The drone flies along the YZ plane while centered at 0 along the X plane. The Y and Z coordinates track the Traqr.

#### [cf_multi_interactive.py](examples/cf_multi_interactive.py)

This script demonstrates real-time interactive control of two Crazyflie drones, coupling the drones' flight to the position of a [Qualisys Traqr](https://www.qualisys.com/accessories/traqr/).

The drones take off and fly circles around Z axis. Their altitude (Z coordinate) tracks the Traqr.

![Robomaster TT](https://qualisys.github.io/qualisys_drone_sdk/qfly_tt.png)

## Robomaster TT

Coming soon...

---

# Resources and Inspirations

- Tutorial on [Building Interactions with the Bitcraze Crazyflie and Motion Capture](https://www.baytas.net/blog/crazyflie) by Mehmet Aydın Baytaş
- Fun project: [Santa's Flying Helpers](https://www.bitcraze.io/2021/12/santas-flying-helpers/) by Bitcraze
- [Overview of different positioning systems](https://www.bitcraze.io/2021/05/positioning-system-overview/) you can use with the Bitcraze Crazyflie
- [Notes on the design of Drone Chi](https://www.bitcraze.io/2019/12/designing-dronechi/), a meditative human-drone interaction experiment by Joseph La Delfa

# Development

Following code contributions, the auto-generated documentation needs to be rebuilt using [pdoc3](https://pdoc3.github.io/).

To re-generate the documentation files and place them correctly into the `docs/` folder that is served to the web, use the commands in Windows:

    del docs\*.html
    pdoc qfly --force --html --output-dir docs
    move .\docs\qfly\* .\docs\