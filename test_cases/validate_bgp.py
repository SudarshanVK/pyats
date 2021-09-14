"""
validate_bgp.py
Verify that the list of BGP neighbors on each devices matches the golden state
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
        # testbed = topology.loader.load(f"{testbed}")
        testbed.connect()


class verify_bgp(aetest.Testcase):
    """
    validate that the list of BGP neighbors on the deice matches the
    list provided in gloden state
    """

    @aetest.test
    def test_bgp(self, testbed, goldenstate, steps):
        # load glodenstate configuration file for validation
        with open(f"{goldenstate}") as gsf:
            gs = yaml.safe_load(gsf)
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            # logger.info (f'{device}')
            with steps.start(
                f"Validate BGP neighbor session status for {device_name}",
                continue_=True,
            ) as step:
                # execute command and parse the output
                bgp_neighbors = device.learn("bgp")
                # intrate through the list of neighbors specified in golden state
                # and validate that the session is established
                for neighbor in gs["bgp_neighbor_list"][f"{device_name}"]:
                    # try to extract bgp peering status of the current neighbor
                    # if not found set step result to failed and break from loop
                    try:
                        bgp_peer_status = bgp_neighbors.info["instance"]["default"][
                            "vrf"
                        ]["default"]["neighbor"][f"{neighbor}"]["session_state"]
                    except:
                        logger.info(f"{device_name} - BGP neighbor validation Failed")
                        logger.info(
                            f"BGP peering configuration not found for {neighbor}"
                        )
                        step.failed()
                        break
                    # if session state was found, validate that the state is established.
                    # if not, set step result to failed
                    if bgp_peer_status == "Established":
                        logger.info(f"{device_name} - BGP neighbor validation Passed")
                    else:
                        logger.info(f"{device_name} - BGP neighbor validation Failed")
                        logger.info(
                            f"BGP peering status for {neighbor} is {bgp_peer_status}"
                        )
                        step.failed()


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """
