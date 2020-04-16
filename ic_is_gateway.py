#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import gateway as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_gateway
short_description: Create or delete public gateway.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A public gateway is a virtual network device associated with a VPC,
    which allows access to the Internet. A public gateway resides in a
    zone and can be connected to subnets in the same zone only.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - The user-defined name for this public gateway.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  floating_ip:
    description:
      - Identifies a floating IP by a unique property (C(IP address)).
    type: str
  zone:
    description:
      - The zone name where this public gateway will be created.
    type: str
    required: true
  vpc:
    description:
      - The VPC this public gateway will serve
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create public gateway with random floating IP
  ic_is_gateway:
    gateway: ibmcloud-public-gateway-baby
    vpc: ibmcloud-vpc-baby
    zone: us-south-3

- name: Create public gateway with defined floating IP
  ic_is_gateway:
    gateway: ibmcloud-public-gateway-baby
    vpc: ibmcloud-vpc-baby
    zone: us-south-3
    floating_ip: 128.128.129.129

- name: Delete public gateway
  ic_is_gateway:
    gateway: ibmcloud-gateway-baby
    vpc: ibmcloud-vpc-baby
    zone: us-south-3
    state: absent
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        floating_ip=dict(
            type='str',
            required=False),
        zone=dict(
            type='str',
            required=True),
        vpc=dict(
            type='str',
            required=True),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    public_gateway = sdk.Gateway()

    gateway = module.params["gateway"]
    resource_group = module.params["resource_group"]
    floating_ip = module.params["floating_ip"]
    zone = module.params["zone"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    check = public_gateway.get_public_gateway(gateway)

    if state == "absent":
        if "id" in check:
            result = public_gateway.delete_public_gateway(gateway)
            if "errors" in result:
                module.fail_json(msg=result["errors"])

            payload = {"public_gateway": gateway, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"public_gateway": gateway, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = public_gateway.create_public_gateway(
            name=gateway,
            resource_group=resource_group,
            floating_ip=floating_ip,
            zone=zone,
            vpc=vpc
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
