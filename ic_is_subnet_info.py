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
module: ic_is_subnet_info
short_description: Retrieve information about subnets.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about subnet from IBM Cloud.
notes:
    - The result contains a list of subnets.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            - Restrict results to subnet with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve subnet list
- ic_is_subnet_info:

# Retrieve subnet list and register the value
- ic_is_subnet_info:
  register: subnets

# Display subnets registered value
- debug:
    var: subnets

# Retrieve a specific subnet by ID or by name
- ic_is_subnet_info:
    subnet: ibmcloud-subnet-baby
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    subnet = sdk.Subnet()

    name = module.params['subnet']

    if name:
        result = subnet.get_subnet(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = subnet.get_subnets()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
