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
module: ic_iam_role_info
short_description: Retrieve IAM roles on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - While managing roles, you may want to retrieve roles and filter by usages.
    This can be done through query parameters. Currently, we only support the
    following attributes: account_id, and service_name.
  - Only roles that match the filter and that the caller has read access to
    are returned. If the caller does not have read access to any roles an empty
    array is returned.
requirements:
  - "ibmcloud-python-sdk"
options:
  role:
    description:
      - The role name or ID.
    type: str
  service
    description:
      - Service name where to list the role.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve system role list
  ic_iam_role_info:

- name: Retrieve specific system role
  ic_iam_role_info:
    role: ibmcloud-role-baby

- name: Retrieve service role list
  ic_iam_role_info:
    service: ibmcloud-service-baby

- name: Retrieve specific system role
  ic_iam_role_info:
    service: ibmcloud-service-baby
    role: ibmcloud-role-baby
'''


def run_module():
    module_args = dict(
        role=dict(
            type='str',
            required=False),
        service=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    iam_role = sdk.Role()

    role = module.params['role']
    service = module.params['service']

    # Retrieve account ID
    account_id = decode_token()['account']['bss']

    if role:
        result = iam_role.get_system_role(account_id, role)
        if "errors" in result:
            module.fail_json(msg=result)
    elif service:
        result = iam_role.get_service_roles(account_id, service)
        if "errors" in result:
            module.fail_json(msg=result)
    elif service and role:
        result = iam_role.get_service_role(account_id, service, role)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = iam_role.get_system_roles(account_id)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
