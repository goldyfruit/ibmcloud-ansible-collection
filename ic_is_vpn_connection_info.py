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
module: ic_is_vpn_connection_info
short_description: Retrieve information about VPN connection.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve information about VPN connection from IBM Cloud.
notes:
  - The result contains a list of connections.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - VPN gateway ID or name.
  connection:
    description:
      - Restrict results to VPN connection with ID or name matching.
'''

EXAMPLES = r'''
# Retrieve VPN connection list
- ic_is_vpn_connection_info:
    gateway: ibmcloud-vpn-gateway-baby

# Retrieve VPN connection list and register the value
- ic_is_vpn_connection_info:
    gateway: ibmcloud-vpn-gateway-baby
  register: connections

# Display connections registered value
- debug:
    var: connections

# Retrieve a specific VPN connection
- ic_is_vpn_connection_info:
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
    name = module.params['connection']

    if name:
        result = vpn.get_vpn_gateway_connection(gateway, name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = vpn.get_vpn_gateway_connections(gateway)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
