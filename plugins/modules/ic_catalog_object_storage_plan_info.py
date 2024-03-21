#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.catalog import catalog_service as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_catalog_object_storage_plan_info
short_description: Retrieve existing catalog object storage plans from IBM Cloud.
author: Maxim Babushkin (@maxbab)
version_added: "2.9"
description:
  - Get a list of existing catalog object storage plans in an account.
notes:
  - The result contains a list of catalog object storage plans.
requirements:
  - "ibmcloud-python-sdk"
options:
  plan:
    description:
      - Restrict results to a plan with name matching.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve catalog object storage plans list
  ic_catalog_object_storage_plan_info:

- name: Retrieve catalog object storage specific plan
  ic_catalog_object_storage_plan_info:
    plan: standard
'''


def run_module():
    module_args = dict(
        plan=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    catalog = sdk.CatalogService()

    plan = module.params['plan']

    if plan:
      result = catalog.get_requested_object_storage_plan(plan)
      if "errors" in result:
        module.fail_json(msg=result)
    else:
      result = catalog.get_object_storage_plans()
      if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
