#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import volume as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_volume_profile_info
short_description: Retrieve information about volume profiles.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about volume profile from IBM Cloud.
notes:
    - The result contains a list of volume profiles.
requirements:
    - "ibmcloud-python-sdk"
options:
    profile:
        description:
            - Restrict results to volume profile with name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve volume profile list
- ic_is_volume_profile_info:

# Retrieve volume profile list and register the value
- ic_is_volume_proile_info:
  register: profiles

# Display profiles registered value
- debug:
    var: profiles

# Retrieve a specific volume profile
- ic_is_volume_profile_info:
    profile: ibmcloud-profile-baby
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

    volume = sdk.Volume()

    name = module.params['profile']

    if name:
        result = volume.get_volume_profile(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = volume.get_volume_profiles()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
