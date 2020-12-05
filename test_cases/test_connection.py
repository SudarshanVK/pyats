"""
test_connection.py
Verify that all devices in the testbed can be successfully connected to.
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

__author__ = "SVK"
__contact__ = ["sudarshan.net09@gmail.com"]
__credits__ = []
__version__ = 1.0

import logging
import yaml

from pyats import aetest
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def assert_golden(self, goldenstate):
        """
        validate that a golden state was provided during execution.
        """
        # make sure network gloden state file is provided
        assert goldenstate, "Goldenstate is not provided!"
        
        #validate that the provided gloden state YAML file is valid
        try:
            with open("golden_state.yaml") as gsf:
                gs = yaml.safe_load(gsf)
        except (yaml.parser.ParserError):
            logger.error("Invalid YAML syntax in provided glodenstate file")
        
        
    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class verify_connected(aetest.Testcase):
    """verify_connected
    Ensure successful connection to all devices in testbed.
    """

    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """
