#!/usr/bin/env python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_vpc_info
short_description: Retrieve information about VPC (Virtual Private Cloud)
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about VPC (Virtual Private Cloud) from IBM Cloud.
notes:
    - The result contains a list of VPC.
requirements:
    - "python >= 3.6"
    - "ibmcloud-python-sdk"
options:
    vpc:
        description:
            - Restrict results to vpc with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve VPC list
- ic_is_vpc_info:

# Retrieve VPC list and register the value
- ic_is_vpc_info:
  register: vpcs

# Display vpcs registered value
- debug:
    var: vpcs

# Retrieve a specific VPC by ID or by name
- ic_is_vpc_info:
    vpc: ibmcloud-vpc-baby
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpc = sdk.Vpc()

    if module.params['vpc']:
        result = vpc.get_vpc(module.params['vpc'])
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = vpc.get_vpcs()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
