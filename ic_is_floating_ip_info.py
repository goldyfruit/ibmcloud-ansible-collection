#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import floating_ip as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_floating_ip_info
short_description: Retrieve information about floating IPs.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about floating IPs from IBM Cloud.
notes:
    - The result contains a list of floating IPs.
requirements:
    - "ibmcloud-python-sdk"
options:
    fip:
        description:
            - Restrict results to floating IP with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve floating IP list
- ic_is_floating_ip_info:

# Retrieve floating IP list and register the value
- ic_is_floating_ip_info:
  register: fips

# Display fips registered value
- debug:
    var: fips

# Retrieve a specific floating IP by ID, by name or by address
- ic_is_floating_ip_info:
    fip: 128.128.129.129
'''


def run_module():
    module_args = dict(
        fip=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    fip = sdk.Fip()

    name = module.params['fip']

    if name:
        result = fip.get_floating_ip(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = fip.get_floating_ips()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
