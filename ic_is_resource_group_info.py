#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import resource_group as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_resource_group_info
short_description: Retrieve information about resource groups.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about resource groups from IBM Cloud.
notes:
    - The result contains a list of resource groups.
requirements:
    - "ibmcloud-python-sdk"
options:
    group:
        description:
            - Restrict results to group with name matching.
        required: false
    account:
        description:
            - Restrict results to resource groups for a specific account.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve resource group list
- ic_is_resource_group_info:

# Retrieve resource group list and register the value
- ic_is_resource_group_info:
  register: resource_groups

# Display resource groups registered value
- debug:
    var: resource_groups

# Retrieve a specific resource group by name
- ic_is_resource_group_info:
    region: us-south

# Retrieve resource groups for a specific account
- ic_is_resource_group_info:
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

    resource = sdk.Resource()

    group = module.params['group']
    account = module.params['account']

    if group:
        result = resource.get_resource_group(group)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    elif account:
        result = resource.get_resource_groups_by_account(account)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = resource.get_resource_groups()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
