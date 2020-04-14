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
module: ic_is_vpn_gateway_info
short_description: Retrieve information about VPN gateway.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve information about VPN gateway from IBM Cloud.
notes:
  - The result contains a list of gateways.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - Restrict results to VPN gateway with ID or name matching.
'''

EXAMPLES = r'''
# Retrieve VPN gateway list
- ic_is_vpn_gateway_info:

# Retrieve VPN gateway list and register the value
- ic_is_vpn_gateway_info:
  register: gateways

# Display VPN gateway registered value
- debug:
    var: gateways

# Retrieve a specific VPN gateway policy
- ic_is_vpn_gateway_info:
    gateway: ibmcloud-vpn-gateway-baby
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

    vpn = sdk.Vpn()

    name = module.params['gateway']

    if name:
        result = vpn.get_vpn_gateway(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = vpn.get_vpn_gateways()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
