"""
validate_bgp.py
Verify that the list of BGP neighbors on each devices matches the golden state
provided.
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

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
        logger.info(
            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
        )
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
        with open(f'{goldenstate}') as gsf:
            gs = yaml.safe_load(gsf)
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            # logger.info (f'{device}')
            with steps.start(
                f"Validate BGP neighbor List for {device_name}", continue_=True
            ) as step:
                # execute command and parse the output
                bgp_neighbors = device.parse("show bgp all neighbors")
                # logger.info(f'{bgp_neighbors}')
                # obtain current list of BGP neighbors from the parsed output
                current_bgp_neighbor_list = bgp_neighbors["list_of_neighbors"]
                # obtain list of BGP neighbors from golden state file
                gs_bgp_neighbor_list = gs['bgp_neighbor_list'][f'{device_name}']
                
                if current_bgp_neighbor_list == gs_bgp_neighbor_list:
                    logger.info(f"{device_name} - BGP neighbor validation Passed")
                else:
                    logger.info(f"{device_name} - BGP neighbor validation Failed")
                    logger.info(f"Expected: {gs_bgp_neighbor_list}")
                    logger.info(f"Current: {current_bgp_neighbor_list}")
                    step.failed()
     
        
class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """
    
# if __name__ == "__main__":
#     # for stand-alone execution
#     from pyats import topology
    
#     # testbed = load('svk_testbed.yaml')
#     aetest.main(testbed=testbed, goldenstate=goldenstate)