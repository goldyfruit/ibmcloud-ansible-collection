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
module: ic_is_quota_definition_info
short_description: Retrieve quota definitions on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Get a list of quota definitions from resource controller.
notes:
  - The result contains a list of quota definitions.
requirements:
  - "ibmcloud-python-sdk"
options:
  quota:
    description:
      - Restrict results to definition with ID or name matching.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve quota definitions list
  ic_is_quota_definition_info:

- name: Retrieve specific quota definition
  ic_is_quota_definition_info:
    quota: ibmcloud-quota-baby
'''


def run_module():
    module_args = dict(
        quota=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource = sdk.Resource()

    quota = module.params['quota']

    if quota:
        result = resource.get_quota_definition(quota)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = resource.get_quota_definitions()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
