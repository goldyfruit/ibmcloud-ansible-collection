#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import key as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_key_info
short_description: Retrieve VPC SSH key on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  -  A key contains a public SSH key which may be installed on instances when
     they are created. Private keys are not stored.
notes:
  - The result contains a list of SSH keys.
requirements:
  - "ibmcloud-python-sdk"
options:
  key:
    description:
      - Restrict results to key with IS or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve key list
  ic_is_key_info:

- name: Retrieve specific key
  ic_is_key_info:
    key: ibmcloud-key-baby
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

    vsi_key = sdk.Key()

    key = module.params['key']

    if key:
        result = vsi_key.get_key(key)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vsi_key.get_keys()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
