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
module: ic_is_security_group_info
short_description: Retrieve information about security groups.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about security groups from IBM Cloud.
notes:
    - The result contains a list of security groups.
requirements:
    - "ibmcloud-python-sdk"
options:
    group:
        description:
            - Restrict results to security group with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve security grouplist
- ic_is_security_group_info:

# Retrieve security group list and register the value
- ic_is_security_group_info:
  register: groups

# Display groups registered value
- debug:
    var: groups

# Retrieve specific security group
- ic_is_security_group_info:
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

    name = module.params['group']

    if name:
        result = security.get_security_group(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = security.get_security_groups()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
