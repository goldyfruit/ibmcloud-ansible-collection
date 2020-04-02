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
module: ic_is_subnet_acl_info
short_description: Retrieve information about subnet's network ACL.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about subnet's network ACL from IBM Cloud.
notes:
    - The result contains network ACL with rules.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            - Subnet name or ID to retrieve the network ACL.
        required: true
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve subnet's network ACL list
- ic_is_subnet_acl_info:
    subnet: ibmcloud-subnet-baby

# Retrieve network ACL attached to a subnet and register the value
- ic_is_subnet_info:
    subnet: ibmcloud-subnet-baby
  register: network_acl

# Display network_acl registered value
- debug:
    var: network_acl
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

    result = subnet.get_subnet_network_acl(name)
    if "errors" in result:
        module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
