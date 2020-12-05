import logging
import json
import yaml
from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)

testbed = load("svk_testbed.yaml")
testbed.connect(log_stdout=False)

with open("golden_state.yaml") as gsf:
    gs = yaml.safe_load(gsf)
    # print(gs)

# device is actually device parameters eg:- device.os - look at the testbed file
# and it will make sense.
for device_name, device in testbed.devices.items():
    print (f"processing host {device_name}")
    logger.info(f"processing host {device_name}")
    # print (device)
    # interface_info = device.learn("interface").info
    # print (interface_info)
    # output = device.learn("routing").info
    # print (json.dumps(output, indent=4))
    
    # use for validating list of neighbors
    # bgp_neighbors = device.parse("show bgp all neighbors")
    # # print (bgp_neighbors)
    # current_bgp_neighbor_list = bgp_neighbors["list_of_neighbors"]
    # gs_bgp_neighbor_list = gs['bgp_neighbor_list'][f'{device_name}']
    # # print (current_bgp_neighbor_list)
    # # print (gs_bgp_neighbor_list)
    # assert current_bgp_neighbor_list == gs_bgp_neighbor_list
    
    # use for validating interface errors
    # output2 = device.parse("show interface stats")
    # print (json.dumps(output2, indent=4))
    
    
    bgp = device.learn('bgp')
    print (bgp.info)