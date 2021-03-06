#!/usr/bin/env python2.7

# Copyright 2015 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


''' Sample usage of function 'interface_configuration_update' to startup an interface.

    Print the function's documentation then invoke the function.
    Apply the function to one interface on one device.
    The device must be connected.
    The interface must be on the 'data plane', not the 'control plane'.
    The interface must be 'down' already.
'''
from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
import os
from basics.interpreter import sys_exit
from basics.interface import management_interface
from basics.interface_configuration import interface_configuration
from basics.interface_configuration import interface_configuration_update
from basics.interface_names import interface_names
from basics.inventory import inventory_connected

shutdown = False

def demonstrate(device_name, interface_config):
    print("Initial configuration:")
    initial = interface_config
    print(initial)
    assert initial.shutdown
    
    print()
    print("Startup interface %s on %s:" % (initial.name, device_name))
    print('interface_configuration_update(' + device_name, initial.name, initial.description, initial.address, initial.netmask, shutdown, sep=', ', end=')\n')
    interface_configuration_update(device_name, initial.name, description=initial.description,
                           address=initial.address, netmask=initial.netmask, shutdown=shutdown)
    print()
    print("Modified configuration:")
    modified = interface_configuration(device_name, initial.name)
    print(modified)
    assert not modified.shutdown

def main():
    print(plain(doc(interface_configuration_update)))
    for device_name in inventory_connected():
        mgmt_name = management_interface(device_name)
        for interface_name in interface_names(device_name):
            # Choose interface on 'data plane' not 'control plane'.
            if interface_name == mgmt_name:
                continue
            interface_config = interface_configuration(device_name, interface_name)
            if not interface_config.address:
                continue
            if not interface_config.shutdown:
                continue
            demonstrate(device_name, interface_config)
            return os.EX_OK
    print("There are no suitable network devices/interfaces. Demonstration cancelled.")
    return os.EX_TEMPFAIL


if __name__ == "__main__":
    sys_exit(main())
