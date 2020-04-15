#!/usr/bin/env python

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
module: ic_is_vpn_cidr_info
short_description: Retrieve information about local/peer CIDRs.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve information about VPN connection's local/peer CIDRs
    from IBM Cloud.
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
'''

EXAMPLES = r'''
# Retrieve peer CIDR list
- ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer

# Retrieve local CIDR list
- ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: local

# Retrieve peer CIDR list and register the value
- ic_is_vpn_cidr_info:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
  register: cidrs

# Display cidrs registered value
- debug:
    var: cidrs

# Retrieve a specific peer CIDR
- ic_is_vpn_cidr_info:
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
    name = module.params['cidr']

    # Split CIDR to get address and length
    if name:
        prefix_address = name.split('/')[0]
        prefix_length = name.split('/')[1]

    if target == "local":
        if name:
            result = vpn.check_vpn_gateway_local_cidr(
              gateway, connection, prefix_address, prefix_length)
            if result and "errors" in result:
                module.fail_json(msg=result["errors"])
        else:
            result = vpn.get_vpn_gateway_local_cidrs(gateway, connection)
            if "errors" in result:
                module.fail_json(msg=result["errors"])
    else:
        if name:
            result = vpn.check_vpn_gateway_peer_cidr(
              gateway, connection, prefix_address, prefix_length)
            if result and "errors" in result:
                module.fail_json(msg=result["errors"])
        else:
            result = vpn.get_vpn_gateway_peer_cidrs(gateway, connection)
            if "errors" in result:
                module.fail_json(msg=result["errors"])

    module.exit_json(change=False, msg="cidr has been found.".format(name))


def main():
    run_module()


if __name__ == '__main__':
    main()
