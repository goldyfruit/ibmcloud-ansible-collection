#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance_fip_info
short_description: Retrieve floating IPs from a VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve floating IPs attached to VSI (Virtual Server
      Instance) on IBM Cloud.
notes:
    - The result contains a list of floating IPs.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance UUID or name.
        required: true
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve floating IPs attached to the VSI
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby

# Retrieve floating IPs and register the value
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby
  register: fips

# Display config registered value
- debug:
    var: fips
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = sdk.Instance()

    name = module.params['instance']

    interfaces = instance.get_instance_interfaces(name)
    if "errors" in interfaces:
        module.fail_json(msg=interfaces)

    nics = []
    fips = {}
    for interface in interfaces["network_interfaces"]:
        data = instance.get_instance_interface_fips(name, interface["id"])
        if "errors" in data:
            module.fail_json(msg=data)
        nics.append(data)
    fips["nics"] = nics

    module.exit_json(**fips)


def main():
    run_module()


if __name__ == '__main__':
    main()
