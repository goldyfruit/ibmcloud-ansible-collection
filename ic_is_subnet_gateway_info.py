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
module: ic_is_subnet_gateway_info
short_description: Retrieve VPC public gateway attached on subnet on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves the public gateway attached to the subnet specified
    by the identifier in the URL.
notes:
  - The result contains public gateway.
requirements:
  - "ibmcloud-python-sdk"
options:
  subnet:
    description:
      - Subnet name or ID .
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Retrieve public gateway attached to subnet
  ic_is_subnet_gateway_info:
    subnet: ibmcloud-subnet-baby
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_subnet = sdk.Subnet()

    subnet = module.params['subnet']

    result = vsi_subnet.get_subnet_public_gateway(subnet)
    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
