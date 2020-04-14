#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+

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
  - Create or delete VPN gateway on IBM Cloud.
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
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Create VPN gateway
- ic_is_vpn_gateway:
    gateway: ibmcloud-vpn-ike-baby
    subnet: ibmcloud-subnet-baby

# Delete VPN gateway
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

    name = module.params['gateway']
    subnet = module.params['subnet']
    resource_group = module.params['resource_group']
    state = module.params["state"]

    if state == "absent":
        result = vpn.delete_gateway(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "gateway {} doesn't exist".format(name)))

        module.exit_json(changed=True, msg=(
            "gateway {} successfully deleted".format(name)))
    else:
        check = vpn.get_vpn_gateway(name)
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpn.create_gateway(
            name=name,
            subnet=subnet,
            resource_group=resource_group,
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
