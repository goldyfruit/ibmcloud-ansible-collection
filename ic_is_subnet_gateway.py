#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_subnet_gateway
short_description: Manage VPC subnet public gateway on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module attaches the public gateway, specified in the request body,
    to the subnet specified by the subnet identifier in the URL. The public
    gateway must have the same VPC and zone as the subnet.
requirements:
  - "ibmcloud-python-sdk"
options:
  subnet:
    description:
      - Subnet name or ID.
    type: str
    required: true
  gateway:
    description:
      - Public gateway name or ID.
    type: str
    required: true
  state:
    description:
      - Should the resource be present, absent, attach or detach.
    type: str
    default: attach
    choices: [present, absent, attach, detach]
'''

EXAMPLES = r'''
- name: Attach public gateway to a subnet
  ic_is_subnet_gateway:
    subnet: ibmcloud-subnet-baby
    gateway: ibmcloud-public-gateway-baby

- name: Detach public gateway from a subnet
  ic_is_subnet_gateway:
    subnet: ibmcloud-subnet-baby
    gateway: ibmcloud-public-gateway-baby
    state: absent
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
        gateway=dict(
            type='str',
            required=True),
        state=dict(
            type='str',
            default='attach',
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_subnet = sdk.Subnet()

    subnet = module.params["subnet"]
    gateway = module.params["gateway"]
    state = module.params["state"]

    check = vsi_subnet.get_subnet_public_gateway(subnet)

    if state == "absent" or state == "detach":
        if "id" in check:
            result = vsi_subnet.detach_public_gateway(subnet)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"public_gateway": gateway, "subnet": subnet,
                       "status": "detached"}
            module.exit_json(changed=True, msg=payload)

        payload = {"public_gateway": gateway, "subnet": subnet,
                   "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vsi_subnet.attach_public_gateway(
            subnet=subnet,
            public_gateway=gateway
        )
        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
