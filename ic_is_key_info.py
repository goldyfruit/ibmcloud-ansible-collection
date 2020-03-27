#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import key as sdk_key


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_key_info
short_description: Retrieve information about SSH keys
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about SSH keys from IBM Cloud.
notes:
    - The result contains a list of SSH keys.
requirements:
    - "ibmcloud-python-sdk"
options:
    key:
        description:
            - Restrict results to key with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve key list
- ic_is_key_info:

# Retrieve key list and register the value
- ic_is_key_info:
  register: keys

# Display keys registered value
- debug:
    var: keys

# Retrieve a specific key by ID or by name
- ic_is_key_info:
    key: ibmcloud-ssh-key
'''


def run_module():
    module_args = dict(
        key=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    key = sdk_key.Key()

    name = module.params['key']

    if name:
        result = key.get_key(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = key.get_keys()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
