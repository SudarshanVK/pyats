"""
test01_testbed_connection_job.py
Verify that all devices in the testbed can be successfully connected to.
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
# for how job files work

__author__ = "SVK"
__contact__ = ["sudarshan.net09@gmail.com"]
__credits__ = []
__version__ = 1.0

import os
import argparse
import yaml

from pyats.easypy import run
from pyats import topology
from genie.testbed import load

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""
    parser = argparse.ArgumentParser()
    parser.add_argument ('--goldenstate',
                         dest = 'goldenstate',
                         help="goldenstate YAML file",
                         default = None)
    
    #parse args
    args, unknown = parser.parse_known_args()

    # run script to validate a golden state is provided and connection to all
    # devices are working.
    test_connection = os.path.join(SCRIPT_PATH, "test_connection.py")
    run(
        testscript=test_connection,
        taskid="Check connection to devices",
        **vars(args),
    )
    
    # run script to check for interface errors
    interface_errors = os.path.join(SCRIPT_PATH, "interface_errors.py")
    run(
        testscript=interface_errors,
        taskid="Check for interface errors",
        **vars(args),
    )
    
    # run script to validate list of BGP neighbors on all devices.
    validate_bgp = os.path.join(SCRIPT_PATH, "validate_bgp.py")
    run(
        testscript=validate_bgp,
        taskid="Validate BGP neighbor list",
        **vars(args),
    )    