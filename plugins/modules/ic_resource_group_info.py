#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_group as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_resource_group_info
short_description: Retrieve available resource groups on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Get a list of all resource groups in an account.
notes:
  - The result contains a list of resource groups.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - Restrict results to group with name matching.
  type: str
  account:
    description:
      - Restrict results to resource groups for specific account.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve resource group list
  ic_resource_group_info:

- name: Retrieve specific resource group
  ic_resource_group_info:
    group: ibmcloud-rg-baby

- name: Retrieve resource group list for specific account
  ic_resource_group_info:
    account: a3d7b8d01e261c24677937c29ab33f3c
'''


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=False),
        account=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource = sdk.ResourceGroup()

    group = module.params['group']
    account = module.params['account']

    if group:
        result = resource.get_resource_group(group)
        if "errors" in result:
            module.fail_json(msg=result)
    elif account:
        result = resource.get_resource_groups_by_account(account)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = resource.get_resource_groups()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
