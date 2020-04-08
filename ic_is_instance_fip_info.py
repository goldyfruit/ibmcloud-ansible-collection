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
      Instance) network interfaces on IBM Cloud.
notes:
    - The result contains a list of floating IPs.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance UUID or name.
        required: true
    fip:
        description:
            - Floating IP name, ID or address.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve floating IPs attached to a VSI
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby

# Retrieve specific floating IP attached to a VSI
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby
    floating_ip: 192.234.192.234

# Retrieve floating IPs and register the value
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby
  register: fips

# Display fips registered value
- debug:
    var: fips
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        floating_ip=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = sdk.Instance()

    name = module.params['instance']
    floating_ip = module.params['floating_ip']

    interfaces = instance.get_instance_interfaces(name)
    if "errors" in interfaces:
        module.fail_json(msg=interfaces["errors"])

    nics = []
    fips = {}
    for interface in interfaces["network_interfaces"]:
        data = instance.get_instance_interface_fips(name, interface["id"])
        if "errors" in data:
            module.fail_json(msg=data["errors"])

        if floating_ip:
            fip = instance.get_instance_interface_fip(name, interface["id"],
                                                      floating_ip)
            if "errors" in data:
                module.fail_json(msg=fip["errors"])

            module.exit_json(**fip)

        nics.append(data)

    fips["nics"] = nics

    module.exit_json(**fips)


def main():
    run_module()


if __name__ == '__main__':
    main()
