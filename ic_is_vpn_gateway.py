#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpn as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_vpn_gateway
short_description: Create or delete VPN gateway.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new VPN gateway.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - The user-defined name for this gateway
    type: str
    required: true
  subnet:
    description:
      - Identifies a subnet by a unique property.
    type: str
  resource_group:
    description:
      - The resource group to use.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create VPN gateway
  ic_is_vpn_gateway:
    gateway: ibmcloud-vpn-gateway-baby
    subnet: ibmcloud-subnet-baby

- name: Delete VPN gateway
- ic_is_vpn_gateway:
    gateway: ibmcloud-vpn-gateway-baby
    state: absent
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        subnet=dict(
            type='str',
            required=False),
        resource_group=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpn = sdk.Vpn()

    gateway = module.params['gateway']
    subnet = module.params['subnet']
    resource_group = module.params['resource_group']
    state = module.params["state"]

    check = vpn.get_vpn_gateway(gateway)

    if state == "absent":
        if "id" in check:
            result = vpn.delete_gateway(gateway)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"gateway": gateway, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"gateway": gateway, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpn.create_gateway(
            name=gateway,
            subnet=subnet,
            resource_group=resource_group,
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
