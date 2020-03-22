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
module: ic_profile_info
short_description: Retrieve information about instance profile(s)
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about instance profile(s) from IBM Cloud.
notes:
    - The result contains a list of instance profiles.
requirements:
    - "python >= 3.5"
    - "ibmcloud-python-sdk"
options:
    profile:
        description:
            - Restrict results to instance profile with name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve all instance profiles list
- ic_profile_info:

# Retrieve all instance profiles and register the value
- ic_profile_info:
  register: profiles

# Display profiles registered value
- debug:
    var: profiles

# Retrieve a specific instance profile by name
- ic_profile_info:
    name: cx2-4x8
'''


def run_module():
    module_args = dict(
        profile=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = ic.Instance()

    if module.params['profile']:
        result = instance.get_instance_profile_by_name(
            module.params['profile'])
        if "errors" in result:
            module.fail_json(msg="instance profile not found")
    else:
        result = instance.get_instance_profiles()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
