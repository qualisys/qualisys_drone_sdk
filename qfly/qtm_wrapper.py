import asyncio
import math
import os
from threading import Thread
import xml.etree.cElementTree as ET

import qtm

from qfly import Pose


class QtmWrapper(Thread):
    """Run QTM connection on its own thread.

    Attributes
    ----------
    body : string
        Name of 6DOF rigid body being tracked
    qtm_ip : string
        IP address of QTM instance
    on_pose: function
        Callback to trigger when pose packet is received

    Methods
    -------
    TBD
    """

    def __init__(self, body, on_pose, qtm_ip="127.0.0.1"):
        Thread.__init__(self)

        self.body = body
        self.qtm_ip = qtm_ip
        self.on_pose = on_pose

        self.tracking_loss = 0

        self._body_idx = None
        self._connection = None
        self._stay_open = True

        self.start()

    def close(self):
        self._stay_open = False
        self.join()

    def run(self):
        asyncio.run(self._life_cycle())

    async def _life_cycle(self):
        await self._connect()
        while(self._stay_open):
            await asyncio.sleep(1)
        await self._close()

    async def _connect(self):
        # Establish connection
        print('[QTM] Connecting to QTM at ' + self.qtm_ip)
        self._connection = await qtm.connect(self.qtm_ip)

        # Quit if QTM unavailable
        if self._connection is None:
            print("[QTM] Could not connect to QTM! Terminating...")
            os._exit(1)

        # Register index of body for 6D tracking
        params_xml = await self._connection.get_parameters(parameters=['6d'])
        xml = ET.fromstring(params_xml)
        for index, body in enumerate(xml.findall("*/Body/Name")):
            if body.text.strip() == self.body:
                self._body_idx = index
                print(
                    f'[QTM] Index for rigid body "{self.body}" is: {self._body_idx}')

        # Quit if body not found
        if self._body_idx is None:
            print(f'[QTM] Rigid body "{self.body}" not found! Terminating...')
            os._exit(1)

        # Assign 6D streaming callback
        try:
            await self._connection.stream_frames(components=['6D'],
                                                 on_packet=self._on_packet)
        except asyncio.TimeoutError:
            print("[QTM] Frame stream TimeoutError! Terminating...")
            os._exit(1)

    def _on_packet(self, packet):
        """
        Process 6D packet stream into Pose object and pass on

        Parameters:
            packet (QRTPacket): Incoming packet from QTM
        """
        # Extract 6D component from packet
        header, component_6d = packet.get_6d()

        # Increment tracking loss if no component found
        if component_6d is None:
            print('[QTM] Packet without 6D component! Moving on...')
            self.tracking_loss += 1
            return

        # Extract relevant body data from 6D component
        body_6d = component_6d[self._body_idx]
        # Create Pose object from 6D data
        pose = Pose.from_qtm_6d(body_6d)
        # Check validity and stream to Crazyflie
        if pose.is_valid():
            self.on_pose(pose)
            self.tracking_loss = 0
        else:
            self.tracking_loss += 1

    async def _close(self):
        await self._connection.stream_frames_stop()
        self._connection.disconnect()
