#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import geo as sdk_geo


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_region_info
short_description: Retrieve information about available regions.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about regions availables on IBM Cloud.
notes:
    - The result contains a list of regions.
requirements:
    - "ibmcloud-python-sdk"
options:
    region:
        description:
            - Restrict results to region with name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve region list
- ic_is_region_info:

# Retrieve region list and register the value
- ic_is_region_info:
  register: regions

# Display regions registered value
- debug:
    var: regions

# Retrieve a specific region by name
- ic_is_region_info:
    region: us-south
'''


def run_module():
    module_args = dict(
        region=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    geo = sdk_geo.Geo()

    name = module.params['region']

    if name:
        result = geo.get_region(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = geo.get_regions()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
