#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import acl as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_acl_info
short_description: Retrieve information about network ACLs.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about network ACLs from IBM Cloud.
notes:
    - The result contains a list of network ACLs.
requirements:
    - "ibmcloud-python-sdk"
options:
    acl:
        description:
            - Restrict results to network ACL with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve network ACL list
- ic_is_acl_info:

# Retrieve network ACL list and register the value
- ic_is_acl_info:
  register: acls

# Display acls registered value
- debug:
    var: acls

# Retrieve a specific network ACL by ID or by name
- ic_is_acl_info:
    acl: ibmcloud-acl-baby
'''


def run_module():
    module_args = dict(
        acl=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    acl = sdk.Acl()

    name = module.params['acl']

    if name:
        result = acl.get_network_acl(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = acl.get_network_acls()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
