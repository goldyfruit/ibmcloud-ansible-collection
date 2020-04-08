#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_security_group_rule_info
short_description: Retrieve information about rules from a security group.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about rules from a security group from IBM Cloud.
notes:
    - The result contains a list of rules.
requirements:
    - "ibmcloud-python-sdk"
options:
    group:
        description:
            - Restrict results to security group with UUID or name matching.
        required: true
    rule:
        description:
            - Restrict results to rule with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve rules from security group
- ic_is_security_group_rule_info:
    group: ibmcloud-sec-group-baby

# Retrieve rules from security group and register the value
- ic_is_security_group_rule_info:
    group: ibmcloud-sec-group-baby
  register: rules

# Display rules registered value
- debug:
    var: rules

# Retrieve specific rule from security group
- ic_is_security_group_rule_info:
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

    name = module.params['group']
    rule = module.params['rule']

    if rule:
        result = security.get_security_group_rule(name, rule)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = security.get_security_group_rules(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
