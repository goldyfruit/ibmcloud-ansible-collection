#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import baremetal as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_baremetal_profile_info
short_description: Retrieve baremetal profiles on IBM Cloud.
author: James Regis (@jamesregis)
version_added: "2.9"
description:
  -  An baremetal instance profile specifies the performance characteristics
     and pricing model for an instance.
notes:
  - The result contains a list of baremetal profiles.
requirements:
  - "ibmcloud-python-sdk"
options:
  profile:
    description:
      - Restrict results to VSI profile with ID or name matching.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve baremetal profile list
  ic_is_baremetal_profile_info:

- name: Retrieve specific baremetal profile
  ic_is_baremetal_profile_info:
    profile: ibmcloud-vsi-profile-baby
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

    vsi_instance = sdk.Baremetal()

    profile = module.params['profile']

    if profile:
        result = vsi_instance.get_server_profile(profile)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vsi_instance.get_server_profiles()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
