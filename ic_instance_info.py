#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import instance as ic


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_instance_info
short_description: Retrieve information about one or more instances
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about instance(s) from IBM Cloud.
notes:
    - The result contains a list of VPC.
requirements:
    - "python >= 3.5"
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Restrict results to instance with UUID or name matching.
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

# Retrieve a specific instance by ID
- ic_instance_info:
    instance: r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = ic.Instance()

    if module.params['instance']:
        result = instance.get_instance_by_name(module.params['instance'])
        if "errors" in result:
            result = instance.get_instance_by_id(module.params['instance'])
            if "errors" in result:
                module.fail_json(msg="instance not found")
    else:
        result = instance.get_instances()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
