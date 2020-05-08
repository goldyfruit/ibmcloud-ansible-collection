#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.iam import policy as sdk
from ibmcloud_python_sdk.auth import decode_token


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_iam_access_policy_info
short_description: Retrieve IAM access policies on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - An IAM policy enables a subject to access a resource. These policies are
    used in access decisions when calling APIs for IAM-enabled services.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - The policy ID.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve access policy list
  ic_iam_access_policy_info:

- name: Retrieve specific access policy
  ic_iam_access_policy_info:
    policy: e7aa06cd-aa6d-4686-a04f-0dd01c43adc1
'''


def run_module():
    module_args = dict(
        policy=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    iam_policy = sdk.Policy()

    policy = module.params['policy']

    # Retrieve account ID
    account_id = decode_token()['account']['bss']

    if policy:
        result = iam_policy.get_access(account_id, policy)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = iam_policy.get_accesses(account_id)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
