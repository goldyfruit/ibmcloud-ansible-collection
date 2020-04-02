#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import gateway as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_gateway_info
short_description: Retrieve information about public gateways.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about public gateways from IBM Cloud.
notes:
    - The result contains a list of public gateways.
requirements:
    - "ibmcloud-python-sdk"
options:
    gateway:
        description:
            - Restrict results to public gateway with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve public gateway list
- ic_is_gateway_info:

# Retrieve public gateway list and register the value
- ic_is_gateway_info:
  register: gateways

# Display gateways registered value
- debug:
    var: gateways

# Retrieve a specific public gateway by ID or by name
- ic_is_gateway_info:
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

    gateway = sdk.Gateway()

    name = module.params['gateway']

    if name:
        result = gateway.get_public_gateway(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = gateway.get_public_gateways()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
