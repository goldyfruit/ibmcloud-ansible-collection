#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_key as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_resource_key_info
short_description: Retrieve available resource keys on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Get a list of all resource keys in an account.
notes:
  - The result contains a list of resource keys.
requirements:
  - "ibmcloud-python-sdk"
options:
  key:
    description:
      - Restrict results to key with name matching.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve resource key list
  ic_is_resource_key_info:

- name: Retrieve specific resource key
  ic_is_resource_key_info:
    key: ibmcloud-rk-baby
'''


def run_module():
    module_args = dict(
        key=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource = sdk.ResourceKey()

    key = module.params['key']

    if key:
        result = resource.get_resource_key(key)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = resource.get_resource_keys()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
