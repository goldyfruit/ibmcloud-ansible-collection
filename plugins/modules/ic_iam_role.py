#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.iam import role as sdk
from ibmcloud_python_sdk.auth import decode_token


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_iam_role
short_description: Manage IAM roles on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A role is a collection of actions that can be taken on a resource.
    There are platform (system), service, and custom roles.
requirements:
  - "ibmcloud-python-sdk"
options:
  role:
    description:
      - The name of the role.
      - First letter should start with an upper case.
    type: str
    required: true
  service_name:
    description:
      - The service name.
    type: str
  display_name:
    description:
      - The display name of the role.
    type: str
  actions:
    description:
      - The actions of the role.
    type: list
  description:
    description:
      - The description of the role.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Add role to only list buckets
  ic_iam_role:
    role: Ibmcloud-role-baby
    service_name: cloud-object-storage
    display_name: "List buckets"
    description: "Role to list COS buckets"
    actions:
      - cloud-object-storage.account.get_account_buckets

- name: Delete role
  ic_iam_role:
    role: Ibmcloud-role-baby
    state: absent
'''


def run_module():
    module_args = dict(
        role=dict(
            type='str',
            required=True),
        service_name=dict(
            type='str',
            required=False),
        display_name=dict(
            type='str',
            required=False),
        description=dict(
            type='str',
            required=False),
        actions=dict(
            type='list',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    iam_role = sdk.Role()

    role = module.params['role']
    service_name = module.params['service_name']
    display_name = module.params['display_name']
    description = module.params['description']
    actions = module.params['actions']
    state = module.params['state']

    # Retrieve account ID
    account_id = decode_token()['account']['bss']

    check = iam_role.get_service_role(account_id, service_name, role)

    if state == "absent":
        if "id" in check:
            result = iam_role.delete_role(role)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"role": role, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)
    else:
        result = iam_role.create_role(
          name=role,
          service_name=service_name,
          display_name=display_name,
          description=description,
          actions=actions
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
