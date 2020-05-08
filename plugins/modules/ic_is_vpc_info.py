#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpc as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_vpc_info
short_description: Retrieve VPC (Virtual Private Cloud) on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all VPCs. A VPC is a virtual network that belongs to an
    account and provides logical isolation from other networks. A VPC is made
    up of resources in one or more zones. VPCs are regional, and each VPC can
    contain resources in multiple zones in a region.
notes:
  - The result contains a list of VPCs.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - Restrict results to vpc with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve VPC list
  ic_is_vpc_info:

- name: Retrieve specific VPC
  ic_is_vpc_info:
    vpc: ibmcloud-vpc-baby
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpc = sdk.Vpc()

    name = module.params['vpc']

    if name:
        result = vpc.get_vpc(name)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vpc.get_vpcs()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
