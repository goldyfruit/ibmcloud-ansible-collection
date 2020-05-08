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
module: ic_is_vpn_connection_info
short_description: Retrieve VPC VPN connections IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all the connections of a particular VPN gateway.
notes:
  - The result contains a list of connections.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - VPN gateway ID or name.
    type: str
    required: true
  connection:
    description:
      - Restrict results to VPN connection with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve VPN connection list
  ic_is_vpn_connection_info:
    gateway: ibmcloud-vpn-gateway-baby

- name: Retrieve a specific VPN connection
  ic_is_vpn_connection_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        connection=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpn = sdk.Vpn()

    gateway = module.params['gateway']
    connection = module.params['connection']

    if connection:
        result = vpn.get_vpn_gateway_connection(gateway, connection)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vpn.get_vpn_gateway_connections(gateway)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
