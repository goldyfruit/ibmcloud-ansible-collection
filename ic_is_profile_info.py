#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_profile_info
short_description: Retrieve information about VSI profiles.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about VSI (Virtual Server Instance) profile from
       IBM Cloud.
notes:
    - The result contains a list of instance profiles.
requirements:
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
# Retrieve instance profile list
- ic_is_profile_info:

# Retrieve instance profiles and register the value
- ic_is_profile_info:
  register: profiles

# Display profiles registered value
- debug:
    var: profiles

# Retrieve a specific instance profile
- ic_is_profile_info:
    profile: cx2-4x8
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

    instance = sdk.Instance()

    name = module.params['profile']

    if name:
        result = instance.get_instance_profile(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = instance.get_instance_profiles()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
