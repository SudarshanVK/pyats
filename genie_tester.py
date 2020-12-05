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
    bgp_neighbors = device.learn('bgp')
    for neighbor in gs['bgp_neighbor_list'][f'{device_name}']:
    #     print (neighbor)
        print (json.dumps(bgp_neighbors.info['instance']['default']['vrf']['default']['neighbor'][f'{neighbor}']['session_state'], indent=4))
    # print (json.dumps(bgp_neighbors, indent=4))
    # current_bgp_neighbor_list = bgp_neighbors["list_of_neighbors"]
    # gs_bgp_neighbor_list = gs['bgp_neighbor_list'][f'{device_name}']
    # print (current_bgp_neighbor_list)
    # print (gs_bgp_neighbor_list)
    
    
    # bgp = device.learn('bgp')
    # print (json.dumps(bgp.info, indent=4))