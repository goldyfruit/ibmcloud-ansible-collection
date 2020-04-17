#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import gateway as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_gateway_info
short_description: Retrieve VPC public gateway on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A public gateway is a virtual network device associated with a VPC,
    which allows access to the Internet. A public gateway resides in a
    zone and can be connected to subnets in the same zone only.
notes:
  - The result contains a list of public gateways.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - Restrict results to public gateway with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve public gateway list
  ic_is_gateway_info:

- name: Retrieve specific public gateway
  ic_is_gateway_info:
    gateway: ibmcloud-gateway-baby
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    public_gateway = sdk.Gateway()

    gateway = module.params['gateway']

    if gateway:
        result = public_gateway.get_public_gateway(gateway)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = public_gateway.get_public_gateways()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
