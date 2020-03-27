#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import volume as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_volume_info
short_description: Retrieve information about volumes.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about volume from IBM Cloud.
notes:
    - The result contains a list of volumes.
requirements:
    - "ibmcloud-python-sdk"
options:
    volume:
        description:
            - Restrict results to volume with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve volume list
- ic_is_volume_info:

# Retrieve volume list and register the value
- ic_is_volume_info:
  register: volumes

# Display volumes registered value
- debug:
    var: volumes

# Retrieve a specific volume by ID or by name
- ic_is_volume_info:
    volume: ibmcloud-volume-baby
'''


def run_module():
    module_args = dict(
        volume=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    volume = sdk.Volume()

    name = module.params['volume']

    if name:
        result = volume.get_volume(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = volume.get_volumes()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
