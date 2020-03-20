#!/usr/bin/env python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_instance_info
short_description: Retrieve information about one or more instance
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about instance from IBM Cloud.
notes:
    - The result contains a list of VPC.
requirements:
    - "python >= 3.5"
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - restrict results to instance with UUID matching
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve all instances list
- ic_instance_info:

# Retrieve all instance list and register the value
- ic_instance_info:
  register: instances

# Display instances registered value
- debug:
    var: instances

# Retrieve a specific instance
- ic_instance_info:
    id: r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765
'''


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import instance


def run_module():
    module_args = dict(
        id=dict(
            type='str',
            required=False),
        name=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.params['id'] is not None:
        result = instance.get_instance_by_id(module.params['id'])
    if module.params['name'] is not None:
        result = instance.get_instance_by_name(module.params['name'])
    else:
        result = instance.get_instances()

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
