#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_subnet_gateway_info
short_description: Retrieve information about subnet's public gateway.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about subnet's public gateway from IBM Cloud.
notes:
    - The result contains public gateway.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            - Subnet name or ID to retrieve the public gateway.
        required: true
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve subnet's public gateway
- ic_is_subnet_gateway_info:
    subnet: ibmcloud-subnet-baby

# Retrieve pubic gateway attached to a subnet and register the value
- ic_is_subnet_info:
    subnet: ibmcloud-subnet-baby
  register: public_gateway

# Display public_gateway registered value
- debug:
    var: public_gateway
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

    subnet = sdk.Subnet()

    name = module.params['subnet']

    result = subnet.get_subnet_public_gateway(name)
    if "errors" in result:
        module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
