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
module: ic_is_vpc_address_prefix_info
short_description: Retrieve VPC address prefix on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all address pool prefixes for a VPC.
notes:
  - The result contains a list of address prefixes.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - VPC name or ID
    type: str
    required: true
  prefix:
    description:
      - Restrict results to address prefix with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve address prefix list
  ic_is_vpc_address_prefix_info:
    vpc: ibmcloud-vpc-baby

- name: Retrieve specific address prefix
  ic_is_vpc_address_prefix_info:
    vpc: ibmcloud-vpc-baby
    prefix: ibmcloud-prefix-baby
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=True),
        prefix=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    sdk_vpc = sdk.Vpc()

    vpc = module.params['vpc']
    prefix = module.params['prefix']

    if prefix:
        result = sdk_vpc.get_address_prefix(vpc, prefix)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = sdk_vpc.get_address_prefixes(vpc)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
