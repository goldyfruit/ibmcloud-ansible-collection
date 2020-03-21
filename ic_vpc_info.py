#!/usr/bin/env python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_vpc_info
short_description: Retrieve information about one or more VPC (Virtual Private Cloud)
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about VPC from IBM Cloud.
notes:
    - The result contains a list of VPC.
requirements:
    - "python >= 3.6"
    - "ibmcloud-python-sdk"
options:
    vpc:
        description:
            - restrict results to vpc with UUID or name matching
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve all VPC list
- ic_vpc_info:

# Retrieve all VPC list and register the value
- ic_vpc_info:
  register: vpcs

# Display vpcs registered value
- debug:
    var: vpcs

# Retrieve a specific VPC by ID or by name
- ic_vpc_info:
    vpc: r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765
'''


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import vpc as ic
import json


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

    vpc = ic.Vpc()

    if module.params['vpc']:
        result = vpc.get_vpc_by_name(module.params['vpc'])
        if "errors" in result:
            result = vpc.get_vpc_by_id(module.params['vpc'])
            if "errors" in result:
                 module.fail_json(msg="vpc not found")
    else:
        result = vpc.get_vpcs()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
