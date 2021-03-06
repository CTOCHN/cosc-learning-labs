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

''' Sample usage of function 'static_route_json_all'.

    Print the function's documentation.
    Apply the function to a network device.
    Print the function output.
    If no routes found then retry with a different network device.
'''

from __future__ import print_function as _print_function
from pydoc import plain
from pydoc import render_doc as doc
import os
from basics.interpreter import sys_exit
from basics.routes import static_route_json_all, inventory_static_route
import json

def demonstrate(device_name):
    ''' Apply function 'static_route_json_all' to the specified device.'''
    print()
    print('static_route_json_all(' + device_name, sep=', ', end=')\n')
    route = static_route_json_all(device_name)
    if route:
        print(json.dumps(route, indent=2, sort_keys=True))
    else:
        print('\t', route)
    return bool(route)

def main():
    ''' Select a device and demonstrate, repeat until information found.'''
    print(plain(doc(static_route_json_all)))
    inventory = inventory_static_route()
    if not inventory:
        print("There are no 'static route' capable devices to examine. Demonstration cancelled.")
    else:
        for device_name in inventory:
            if demonstrate(device_name):
                return os.EX_OK
    return os.EX_TEMPFAIL

if __name__ == "__main__":
    sys_exit(main())
