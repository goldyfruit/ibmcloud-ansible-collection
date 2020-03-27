#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk_instance


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance_info
short_description: Retrieve information about VSI (Virtual Server Instance).
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about VSI (Virtual Server Instance) from IBM Cloud.
notes:
    - The result contains a list of instances.
requirements:
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
- ic_is_instance_info:

# Retrieve all instance list and register the value
- ic_is_instance_info:
  register: instances

# Display instances registered value
- debug:
    var: instances

# Retrieve a specific instance by ID
- ic_is_instance_info:
    instance: ibmcloud-vsi-ansible
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

    instance = sdk_instance.Instance()

    name = module.params['instance']

    if name:
        result = instance.get_instance(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = instance.get_instances()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
