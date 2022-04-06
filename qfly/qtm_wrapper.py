import asyncio
import os
from threading import Thread
import xml.etree.cElementTree as ET

import qtm

from qfly import Pose


class QtmWrapper(Thread):
    """Run QTM connection on its own thread."""

    def __init__(self, cf_body_name, qtm_ip="127.0.0.1"):
        Thread.__init__(self)

        self.bodyToIdx = {}
        self.cf_body_name = cf_body_name
        self.connection = None
        self.on_cf_pose = None
        self.qtm_ip = qtm_ip
        self.tracking_loss = 0
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
        print('Connecting to QTM at ' + self.qtm_ip)
        self.connection = await qtm.connect(self.qtm_ip)

        if self.connection == None:
            print("Could not connect to QTM! Terminating...")
            os._exit(1)

        params_xml = await self.connection.get_parameters(parameters=['6d'])
        xml = ET.fromstring(params_xml)
        for index, body in enumerate(xml.findall("*/Body/Name")):
            self.bodyToIdx[body.text.strip()] = index
        print('QTM 6DOF bodies and indexes: ' + str(self.bodyToIdx))

        # Check if all the bodies are there

        if self.cf_body_name in self.bodyToIdx:
            print("Rigid body '" + self.cf_body_name +
                  "' found in QTM 6DOF bodies.")
        else:
            print("Rigid body '" + self.cf_body_name +
                  "' not found in QTM 6DOF bodies!")
            print("Aborting...")
            os._exit(1)

        try:
            await self.connection.stream_frames(components=['6d', '6deuler'],
                                                on_packet=self._on_packet)
        except asyncio.TimeoutError:
            print("QTM connection frame stream timed out.")
            print("Aborting...")
            os._exit(1)

    def _on_packet(self, packet):
        # We need the 6d component to send full pose to Crazyflie,
        # and the 6deuler component for convenient calculations
        header, component_6d = packet.get_6d()
        header, component_6deuler = packet.get_6d_euler()

        if component_6d is None:
            print('No 6d component in QTM packet!')
            return

        if component_6deuler is None:
            print('No 6deuler component in QTM packet!')
            return

        # Get 6DOF data for Crazyflie
        cf_6d = component_6d[self.bodyToIdx[self.cf_body_name]]
        # Store in temp until validity is checked
        cf_pose = Pose.from_qtm_6d(cf_6d)
        # Check validity and stream to Crazyflie
        if cf_pose.is_valid():
            if self.on_cf_pose:
                self.on_cf_pose(cf_pose)
                self.tracking_loss = 0
        else:
            self.tracking_loss += 1

    async def _close(self):
        await self.connection.stream_frames_stop()
        self.connection.disconnect()
