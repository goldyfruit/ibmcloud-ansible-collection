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
module: ic_is_security_group_rule_info
short_description: Retrieve VPC security group rules on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all the security group rules for a particular security
    group. These rules define what traffic the security group permits.
    Security group rules are stateful, such that reverse traffic in response
    to allowed traffic is automatically permitted.
notes:
  - The result contains a list of rules.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - Security group ID or name.
    type: str
    required: true
  rule:
    description:
      - Restrict results to rule with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve rules from security group
  ic_is_security_group_rule_info:
    group: ibmcloud-sec-group-baby

- name: Retrieve specific rule from security group
  ic_is_security_group_rule_info:
    group: ibmcloud-sec-group-baby
    rule: ibmcloud-sec-group-rule-baby
'''


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=True),
        rule=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    security = sdk.Security()

    group = module.params['group']
    rule = module.params['rule']

    if rule:
        result = security.get_security_group_rule(group, rule)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = security.get_security_group_rules(group)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
