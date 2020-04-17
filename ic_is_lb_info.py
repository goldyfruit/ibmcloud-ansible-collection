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
module: ic_is_lb_info
short_description: Retrieve VPC load balancers on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves a paginated list of all load balancers that belong
    to this account.
notes:
  - The result contains a list of load balancers.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Restrict results to load balancer with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve load balancer list
  ic_is_lb_info:

- name: Retrieve specific load balancer
  ic_is_lb_info:
    lb: ibmcloud-lb-baby
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']

    if lb:
        result = loadbalancer.get_lb(lb)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = loadbalancer.get_lbs()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
