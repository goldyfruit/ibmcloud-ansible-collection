#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_subnet_info
short_description: Retrieve VPC subnets on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all subnets in the region. Subnets are contiguous ranges
    of IP addresses specified in CIDR block notation. Each subnet is within a
    particular zone and cannot span multiple zones or regions.
notes:
  - The result contains a list of subnets.
requirements:
  - "ibmcloud-python-sdk"
options:
  subnet:
    description:
      - Restrict results to subnet with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve subnet list
  ic_is_subnet_info:

- name: Retrieve a specific subnet
  ic_is_subnet_info:
    subnet: ibmcloud-subnet-baby
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_subnet = sdk.Subnet()

    subnet = module.params['subnet']

    if subnet:
        result = vsi_subnet.get_subnet(subnet)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vsi_subnet.get_subnets()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
