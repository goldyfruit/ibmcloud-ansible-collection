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
module: ic_is_vpn_cidr_info
short_description: Retrieve VPC VPN local or peer CIDRs on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all local or peer CIDRs for the resource specified by
    the identifier in the URL.
notes:
  - The result contains a list of local or peer CIDRs.
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
      - VPN connection ID or name.
    type: str
    required: true
  target:
    description:
      - Retrieve local or peer CIDRs.
    type: str
    default: local
    choices: [local, peer]
  cidr:
    description:
      - Restrict results to specific CIDR.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve peer CIDR list
  ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer

- name: Retrieve local CIDR list
  ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: local

- name Retrieve specific peer CIDR
  ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
    cidr: 192.168.1.0/24
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        connection=dict(
            type='str',
            required=True),
        target=dict(
            type='str',
            default='local',
            choices=['local', 'peer']),
        cidr=dict(
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
    target = module.params['target']
    cidr = module.params['cidr']

    # Split CIDR to get address and length
    if cidr:
        prefix_address = cidr.split('/')[0]
        prefix_length = cidr.split('/')[1]

    if target == "local":
        if cidr:
            result = vpn.check_vpn_gateway_local_cidr(
              gateway, connection, prefix_address, prefix_length)
            if result and "errors" in result:
                module.fail_json(msg=result)
        else:
            result = vpn.get_vpn_gateway_local_cidrs(gateway, connection)
            if "errors" in result:
                module.fail_json(msg=result)
    else:
        if cidr:
            result = vpn.check_vpn_gateway_peer_cidr(
              gateway, connection, prefix_address, prefix_length)
            if result and "errors" in result:
                module.fail_json(msg=result)
        else:
            result = vpn.get_vpn_gateway_peer_cidrs(gateway, connection)
            if "errors" in result:
                module.fail_json(msg=result)

    payload = {"cidr": cidr, "target": target, "status": "found"}
    module.exit_json(change=False, msg=payload)


def main():
    run_module()


if __name__ == '__main__':
    main()
