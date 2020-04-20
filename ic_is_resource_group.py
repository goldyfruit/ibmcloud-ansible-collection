#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import resource_group as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_resource_group
short_description: Manage VPC resource groups on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new resource group in an account.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - The new name of the resource group.
    type: str
    required: true
  account_id:
    description:
      - The account id of the resource group.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create resource group
  ic_is_resource_group:
    group: ibmcloud-resource-group-new-baby
    account_id: 9aa205e454574e8484b3ca8c2ff33d83

- name: Delete resource group
  ic_is_key:
    group: ibmcloud-resource-group-new-baby
    account_id: 9aa205e454574e8484b3ca8c2ff33d83
    state: absent
'''


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=True),
        account_id=dict(
            type='str',
            required=True),
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

    resource = sdk.Resource()

    group = module.params['group']
    account_id = module.params["account_id"]
    state = module.params["state"]

    check = resource.get_resource_group(group)

    if state == "absent":
        if "id" in check:
            result = resource.delete_group(group)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"resource_group": group, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"resource_group": group, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = resource.create_group(
            group=group,
            account_id=account_id
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
