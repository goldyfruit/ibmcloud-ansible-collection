#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_instance_fip_info
short_description: Retrieve attached floating IPs from a VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve attached floating IPs from a VSI (Virtual Server Instance)
    on IBM Cloud.
notes:
  - The result contains a list of floating IPs.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - Instance UUID or name.
    type: str
    required: true
  fip:
    description:
      - Floating IP name, ID or address.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve floating IPs from a VSI
  ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby

- name: Retrieve specific floating IP from a VSI
- ic_is_instance_fip_info:
    instance: ibmcloud-vsi-baby
    floating_ip: 128.128.129.129
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

    vsi_instance = sdk.Instance()

    instance = module.params['instance']
    floating_ip = module.params['floating_ip']

    interfaces = vsi_instance.get_instance_interfaces(instance)
    if "errors" in interfaces:
        module.fail_json(msg=interfaces["errors"])

    nics = []
    fips = {}
    for interface in interfaces["network_interfaces"]:
        data = vsi_instance.get_instance_interface_fips(instance,
                                                        interface["id"])
        if "errors" in data:
            module.fail_json(msg=data["errors"])

        if floating_ip:
            fip = vsi_instance.get_instance_interface_fip(instance,
                                                          interface["id"],
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
