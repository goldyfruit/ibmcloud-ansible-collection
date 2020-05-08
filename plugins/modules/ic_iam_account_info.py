#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.auth import decode_token


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_iam_account_info
short_description: Retrieve information about IAM account on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module decodes information from IAM JWT token
notes:
  - The result contains a token.
requirements:
  - "ibmcloud-python-sdk"
options:
  account_id_only:
    description:
      - Return only the account ID.
    type: bool
    choices: [true, false]
'''

EXAMPLES = r'''
- name: Retrieve account details
  ic_iam_account_info:
'''


def run_module():
    module_args = dict(
        account_id_only=dict(
            type='bool',
            default=False,
            choices=[True, False],
            required=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    account_id_only = module.params['account_id_only']

    result = decode_token()
    if "errors" in result:
        module.fail_json(msg=result)

    if account_id_only:
        payload = {"account_id": result["account"]["bss"]}
        module.exit_json(change=False, msg=payload)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
