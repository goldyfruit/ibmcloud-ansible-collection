#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_security_group_info
short_description: Retrieve VPC security groups on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all existing security groups. Security groups provide
    a convenient way to apply IP filtering rules to instances in the
    associated VPC. With security groups, all traffic is denied by default,
    and rules added to security groups define which traffic the security group
    permits. Security group rules are stateful such that reverse traffic in
    response to allowed traffic is automatically permitted.
notes:
  - The result contains a list of security groups.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - Restrict results to security group with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve security group list
  ic_is_security_group_info:

- Retrieve specific security group
  ic_is_security_group_info:
    group: ibmcloud-sec-group-baby
'''


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    security = sdk.Security()

    group = module.params['group']

    if group:
        result = security.get_security_group(group)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = security.get_security_groups()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
