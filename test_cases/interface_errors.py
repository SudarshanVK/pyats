"""
interface_errors.py
Verify that there are no CRC's on any interfaces
provided.
"""
__author__ = "SVK"
__contact__ = ["sudarshan.net09@gmail.com"]
__credits__ = []
__version__ = 1.0

import logging
import yaml

from genie.testbed import load
from genie.utils import Dq
from pyats import aetest
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def load_testbed(self, testbed):

        # Convert pyATS testbed to Genie Testbed
        logger.info("Loading testbed file")
        testbed = load(testbed)
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):

        logger.info("Establishing connection to devices in the Testbed file")
        # testbed = topology.loader.load(f"{testbed}")
        testbed.connect()


class int_err(aetest.Testcase):
    """
    validate that there are no in_errors or out_errors or crc_errors in
    any of the interfaces for each device.
    """

    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.learnt_interfaces = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info

    @aetest.test
    def test(self, steps):
        # Loop over every device with learnt interfaces
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for Interface Errors on {device_name}", continue_=True
            ) as device_step:

                # Loop over every interface that was learnt
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:

                        # Verify that this interface has "counters" (Loopbacks Lack Counters on some platforms)
                        if "counters" in interface.keys():
                            # look for error counters with value greater than 0
                            # if found, log and fail the step
                            if (
                                interface["counters"]["in_errors"] > 0
                                or interface["counters"]["in_crc_errors"] > 0
                                or interface["counters"]["out_errors"] > 0
                            ):
                                logger.info(
                                    f"Interface {interface} error counters check Failed"
                                )
                                logger.info(
                                    f"In error = {interface['counters']['in_error']}"
                                )
                                logger.info(
                                    f"CRC error = {interface['counters']['in_crc_error']}"
                                )
                                logger.info(
                                    f"Out error = {interface['counters']['out_error']}"
                                )
                                step.failed()
                            # If no errors found, log and mark test as Passes
                            else:
                                logger.info("Interface error validation Passed")
                        else:
                            # If the interface has no counters, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} missing counters"
                            )


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """
