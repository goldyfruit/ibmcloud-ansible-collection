#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import loadbalancer as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_lb_listener_info
short_description: Retrieve VPC listeners from load balancer on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves a list of all listeners that belong to the load
    balancer.
notes:
  - The result contains a list of listeners.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name or ID.
    type: str
    required: true
  listener:
    description:
      - Restrict results to listener with UUID matching.
    type: str
  port:
    description:
      - Restrict results to listener with port matching.
    type: int
'''

EXAMPLES = r'''
- name: Retrieve listener list from load balancer
  ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby

- name: Retrieve specific listener from load balancer
  ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby
    listener: ibmcloud-lb-listener-baby

- name: Retrieve specific listener from load balancer by using port
  ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby
    port: 443
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        listener=dict(
            type='str',
            required=False),
        port=dict(
            type='int',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']
    id = module.params['listener']
    port = module.params['port']

    if id:
        listener = id
    elif port:
        listener = port

    if listener:
        result = loadbalancer.get_lb_listener(lb, listener)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = loadbalancer.get_lb_listeners(lb)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
